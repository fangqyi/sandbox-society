using MonoBehaviorExtension;
using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class Character: UnityModule 
{

   public int id;
   public int r = 0;
   public int c = 0;

   public Vector3    attackPos;
   public Quaternion attackRot;

   public GameObject target;
   public GameObject attack;
   public Vector3 forward;
   public Vector3 up;
   
   // light communication 
   public Shader lightShader;
   public uint commType;
   public Dictionary<int, Color> commColor;
   public Dictionary<int, Color> commMKGlowColor;
   public Dictionary<int, Color> commMKGlowTexColor;

   public int rOld = 0;
   public int cOld = 0;
   public bool alive = true;


   public string name;
   public int level = 1;

   float start;
   Vector3 orig;

   public SkillGroup skills;
   public ResourceGroup resources;
   public Overheads overheads;
   public float disTool2Agent = 0.5f;
   public float disTool2Ground = 0.5f;
   public float scaleTool = 0.5f;

   // tool prefabs
   static private String toolFilepath = "OneOffDesign/Lowpoly Medieval Fantasy Weapons/Prefabs/";
   static public GameObject prefShield;
   static public GameObject prefSword;
   static public GameObject prefPickaxe;
   static public GameObject prefHatchet;
   
   //tool gameobjects
   public GameObject shield;
   public GameObject sword;
   public GameObject pickaxe;
   public GameObject hatchet;

   public bool hasShield;
   public bool hasSword;
   public bool hasPickaxe;
   public bool hasHatchet;
   
   public static void LoadToolPrefabs(){
      prefPickaxe = Resources.Load(toolFilepath + "Pref_PickAxe_A") as GameObject;
      prefHatchet = Resources.Load(toolFilepath + "Pref_Hatchet_A") as GameObject;
      prefShield = Resources.Load(toolFilepath + "Pref_RoundShield_A") as GameObject; 
      prefSword = Resources.Load(toolFilepath + "Pref_ShortSword_A") as GameObject;
   }

   //Load the OBJ shader and materials
   public void NNObj(Color ball, Color rod_bottom, Color rod_top)
   {
      MeshRenderer nn = this.transform.GetChild(0).GetChild(0).GetComponent<MeshRenderer>();
      nn.materials[0].SetColor("_Color", ball);
      nn.materials[1].SetColor("_Color", rod_bottom);
      nn.materials[2].SetColor("_Color", rod_top);
   }

   //Create the overhead UI
   public void Overheads(string name, Color color)
   {
      this.overheads.name = name;
      this.resources = this.overheads.resources;
      this.overheads.color = color;
      this.overheads.player = this;
   }

   public void Init(Dictionary<int, GameObject> players,
         Dictionary<int, GameObject> npcs, int iden, object packet) {
      this.orig = this.transform.position;
      this.start = Time.time;
      this.id = iden;

      object basePacket = Unpack("base", packet);
      string name = (string)Unpack("name", basePacket);

      Color ball        = hexToColor((string)Unpack("color", basePacket));
      Color rod_bottom  = hexToColor((string)UnpackList(new List<string> { "loadout", "platelegs", "color" }, packet));
      Color rod_top     = hexToColor((string)UnpackList(new List<string> { "loadout", "chestplate", "color" }, packet));

      //OBJ model and overheads
      this.NNObj(ball, rod_bottom, rod_top);
      this.Overheads(name, ball);
      //this.LoadToolPrefabs();

      initToolStatus();

      this.UpdatePlayer(players, npcs, packet);
      this.UpdatePos(false);

      // light communication color     
   }

   public void SetColors() {
      this.commColor = new Dictionary<int, Color>();
      this.commColor.Add(1, hexToColor("FF0000"));
      this.commColor.Add(2, hexToColor("FFF70D"));
      this.commColor.Add(3, hexToColor("0100D9"));

      this.commMKGlowColor = new Dictionary<int, Color>();
      this.commMKGlowColor.Add(1, hexToColor("FF0000"));
      this.commMKGlowColor.Add(2, hexToColor("F1EC03"));
      this.commMKGlowColor.Add(3, hexToColor("11A7EE"));

      this.commMKGlowTexColor = new Dictionary<int, Color>();
      this.commMKGlowTexColor.Add(1, hexToColor("E75E10"));
      this.commMKGlowTexColor.Add(2, hexToColor("FF9800"));
      this.commMKGlowTexColor.Add(3, hexToColor("10E77A"));
   }

   public void UpdateUI()
   {
      this.skills.UpdateUI();
      this.resources.UpdateUI();

      GameObject UIName = GameObject.Find("UI/Canvas/Panel/Name");
      TextMeshProUGUI uiName = UIName.GetComponent<TextMeshProUGUI>();

      uiName.color = this.overheads.playerName.color;
      uiName.text = this.overheads.playerName.text;
   }

   public static void UpdateStaticUI()
   {
      PlayerResources.UpdateDeadUI();
   }

   void Update()
   {
      if (!this.alive) {
         this.DeathAnimation();
      } 
      this.UpdatePos(true);
      this.UpdateAttack();
      this.updateToolForward();
      this.updateToolPos();
   }

   public void UpdatePos(bool smooth)
   {
      Vector3 orig = new Vector3(this.rOld, 0, this.cOld);
      Vector3 targ = new Vector3(this.r, 0, this.c);
      if (smooth)
      {
         this.transform.position = Vector3.Lerp(orig, targ, Client.tickFrac);
      }
      else
      {
         this.transform.position = targ;
      }

      //Turn to target instead of move direction
      if (this.target != null)
      {
         targ = this.target.transform.position;
      }
      this.transform.forward = Vector3.RotateTowards(this.forward, orig - targ, (float)Math.PI * Client.tickFrac, 0f);
   }

   void UpdateTools(bool isSword, bool isShield, bool isHatchet, bool isPickaxe){
      Debug.Log("Check for swords... Current: "+this.hasSword);
      Debug.Log("Sword New: "+isSword);
      Debug.Log("Sword agent current pos: "+ this.transform.position.x + ", " + this.transform.position.y + ", " + this.transform.position.z);
      if (isSword != this.hasSword){
         this.hasSword = isSword;
         if (this.hasSword){
            Vector3 pos = new Vector3(this.transform.position.x + this.disTool2Agent, this.transform.position.y + disTool2Ground, this.transform.position.z);
            Debug.Log("Sword agent new pos: "+ pos.x + ", " + pos.y + ", " + pos.z);
            this.sword = GameObject.Instantiate(prefSword, pos, Quaternion.identity) as GameObject;
            this.sword.transform.localScale *= scaleTool;
            Debug.Log("Sword added");
         }
         else{
            GameObject.Destroy(this.sword);
            Debug.Log("Sword destroyed");
         }
      }
      if (isShield != this.hasShield){
         this.hasShield = isShield;
         if (this.hasShield){
            Vector3 pos = new Vector3(this.transform.position.x - this.disTool2Agent, this.transform.position.y + disTool2Ground, this.transform.position.z);
            this.shield = GameObject.Instantiate(prefShield, pos, Quaternion.identity) as GameObject;
            this.shield.transform.localScale *= scaleTool;
         }
         else{
            GameObject.Destroy(this.shield);
         }
      }
      if (isHatchet != this.hasHatchet){
         this.hasHatchet = isHatchet;
         if (this.hasHatchet){
            Vector3 pos = new Vector3(this.transform.position.x, this.transform.position.y + disTool2Ground, this.transform.position.z + this.disTool2Agent);
            this.hatchet = GameObject.Instantiate(prefHatchet, pos, Quaternion.identity) as GameObject;
            this.hatchet.transform.localScale *= scaleTool;
         }
         else{
            GameObject.Destroy(this.hatchet);
         }
      }
      if (isPickaxe != this.hasPickaxe){
         this.hasPickaxe = isPickaxe;
         if (this.hasPickaxe){
            Vector3 pos = new Vector3(this.transform.position.x, this.transform.position.y + disTool2Ground, this.transform.position.z - this.disTool2Agent);
            this.pickaxe = GameObject.Instantiate(prefPickaxe, pos, Quaternion.identity) as GameObject;
            this.pickaxe.transform.localScale *= scaleTool;
         }
         else{
            GameObject.Destroy(this.pickaxe);
         }
      }
   }

   public void updateToolForward(){
      if (this.hasSword){
         this.sword.transform.forward = this.transform.forward;
      }
      if (this.hasShield){
         this.shield.transform.forward = this.transform.forward;
      }
      if (this.hasHatchet){
         this.hatchet.transform.forward = this.transform.forward; 
      }
      if (this.hasPickaxe){
         this.pickaxe.transform.forward = this.transform.forward; 
      }
   }

   public void updateToolPos(){
      if (this.hasSword){
         this.sword.transform.position = new Vector3(this.transform.position.x + this.disTool2Agent, this.transform.position.y + disTool2Ground, this.transform.position.z);
      }
      if (this.hasShield){
         this.shield.transform.position = new Vector3(this.transform.position.x - this.disTool2Agent, this.transform.position.y + disTool2Ground, this.transform.position.z);
      }
      if (this.hasHatchet){
         this.hatchet.transform.position = new Vector3(this.transform.position.x, this.transform.position.y + disTool2Ground, this.transform.position.z + this.disTool2Agent);
      }
      if (this.hasPickaxe){
         this.pickaxe.transform.position = new Vector3(this.transform.position.x, this.transform.position.y + disTool2Ground, this.transform.position.z - this.disTool2Agent);
      }
   }

   void destroyTools(){
      if (this.hasSword){
         GameObject.Destroy(this.sword);
      }
      if (this.hasShield){
         GameObject.Destroy(this.shield);      
      }
      if (this.hasHatchet){
         GameObject.Destroy(this.hatchet);
      }
      if (this.hasPickaxe){
         GameObject.Destroy(this.pickaxe);
      }
   }

   public void DeathAnimation()
   {
      this.transform.GetChild(0).transform.up = Vector3.RotateTowards(this.up, this.transform.right, (float)Math.PI/2f * Client.tickFrac, 0f);
   }


   public void UpdateAttack()
   {
      if (this.attack == null || this.target == null)
      {
         return;
      }

      //this.attack.transform.position = Vector3.Lerp(this.transform.position, this.target.transform.position, Client.tickFrac) + 3 * Vector3.up / 4;
      //this.attack.transform.position = Vector3.Lerp(this.attackPos, this.target.transform.position, Client.tickFrac);

      //this.attack.transform.rotation = Quaternion.LookRotation(this.target.transform.position - this.attack.transform.position);
      //this.attack.transform.rotation = Quaternion.RotateTowards(this.attackRot, this.attackTarg, this.attackDelta * Client.tickFrac);

      //this.attackTarg   = Quaternion.LookRotation(this.target.transform.position + (this.target.transform.localScale.x * 3 * Vector3.up / 4) - this.attackPos);
      //this.attackRot    = this.attackTarg;
      this.attack.transform.rotation = this.AttackRotation();
   }

   public void UpdatePlayer(Dictionary<int, GameObject> players,
         Dictionary<int, GameObject> npcs, object ent) {
      this.orig    = this.transform.position;
      this.forward = this.transform.forward;
      this.up      = this.transform.up;
      this.start   = Time.time;

      this.alive = Convert.ToBoolean(Unpack("alive", ent));

      //Position
      object entBase = Unpack("base", ent);
      this.rOld = this.r;
      this.cOld = this.c;

      this.r = Convert.ToInt32(UnpackList(new List<string> { "r" }, entBase));
      this.c = Convert.ToInt32(UnpackList(new List<string> { "c" }, entBase));

      //Skills
      object skills = Unpack("skills", ent);
      this.skills.UpdateSkills(skills);
      this.level = Convert.ToInt32(Unpack("level", skills));

      //Attack
      if (this.attack != null)
      {
         Destroy(this.attack);
         this.target = null;
      }

      Dictionary<string, object> hist = Unpack("history", ent) as Dictionary<string, object>;
      int damage = Convert.ToInt32(UnpackList(new List<string> { "damage" }, hist));

      this.overheads.UpdateDamage(damage);
      this.overheads.UpdateOverheads(this);

      //Handle attacks
      if (hist.ContainsKey("attack"))
      {

         object attk = Unpack("attack", hist);
         string style = Unpack("style", attk) as string;
         object targ = Unpack("target", attk);
         int targs = Convert.ToInt32(targ);

         //Handle targets
         if (players.ContainsKey(targs))
         {
            this.target = players[targs];
         } else if (npcs.ContainsKey(targs)) {
            this.target = npcs[targs];
         } else {
            return;
         }

         GameObject attackPrefab = Resources.Load("Prefabs/" + style) as GameObject;

         this.attackPos    = this.transform.position + (
               this.transform.localScale.x * 6 * Vector3.up / 4);
         this.attack       = GameObject.Instantiate(
               attackPrefab, this.attackPos, this.AttackRotation());
      }

      // light-based communication
      // foreach (var pair in hist) {
      //    Debug.Log(pair.Key + ", " + pair.Value);
      // }
      if (hist.ContainsKey("communication")){
         object comm = Unpack("communication", hist);
         object type = Unpack("color", comm);
         this.commType = Convert.ToUInt32(type);
         updateCommunicationShader();
      }

      //if (hist.ContainsKey("technologyStatus")){
      //   object tools = Unpack("technologyStatus", hist);
      //   bool isSword = Convert.ToBoolean(Unpack("sword_status", tools));
      //   bool isShield = Convert.ToBoolean(Unpack("shield_status", tools));
      //   bool isHatchet = Convert.ToBoolean(Unpack("hoe_status", tools));
      //   bool isPickaxe = Convert.ToBoolean(Unpack("improved_hoe_status", tools));
      //   UpdateTools(isSword, isShield, isHatchet, isPickaxe);
      //}
      UpdateTools(true, true, true, true);
      
   }

   void updateCommunicationShader(){
      if (this.lightShader == null){
         this.lightShader = Shader.Find("MK/Glow/Selective/Legacy/Transparent/Diffuse");
      }
      MeshRenderer nn = this.transform.GetChild(0).GetChild(0).GetComponent<MeshRenderer>();

      // if (this.commColor == null) {  // initialize color dictionary
      //    this.SetColors();
      // }

      if (this.commType == 0){  // no light communication
          nn.materials[0].shader = null;  // TODO: make it compatible with existing shader
      }
      else{
         nn.materials[0].shader = this.lightShader;
         nn.materials[0].SetColor("_Color", intToColor(this.commType));
         nn.materials[0].SetColor("_MKGlowColor", intToColor(this.commType));
         nn.materials[0].SetColor("_MKGlowTexColor", intToColor(this.commType));
         nn.materials[0].SetFloat("_MKGlowPower", (float) 4.0);
      }
   }

   void initToolStatus(){
      this.hasHatchet = false;
      this.hasPickaxe = false;
      this.hasSword = false;
      this.hasShield = false;
   }

   
   public Quaternion AttackRotation() {
      return Quaternion.LookRotation(
            this.target.transform.position + (
            this.target.transform.localScale.x * 3 * Vector3.up / 4) - this.attackPos);
   }
   
   public void Delete()
   {
      GameObject.Destroy(this.overheads.gameObject);
      GameObject.Destroy(this.overheads);

      if (this.attack != null)
      {
         GameObject.Destroy(this.attack);
      }
      destroyTools();
   }

   //Random function off Unity forums
   public static Color hexToColor(string hex)
   {
      hex = hex.Replace("0x", "");//in case the string is formatted 0xFFFFFF
      hex = hex.Replace("#", "");//in case the string is formatted #FFFFFF
      byte a = 255;//assume fully visible unless specified in hex
      byte r = byte.Parse(hex.Substring(0, 2), System.Globalization.NumberStyles.HexNumber);
      byte g = byte.Parse(hex.Substring(2, 2), System.Globalization.NumberStyles.HexNumber);
      byte b = byte.Parse(hex.Substring(4, 2), System.Globalization.NumberStyles.HexNumber);
      //Only use alpha if the string has enough characters
      if (hex.Length == 8)
      {
         a = byte.Parse(hex.Substring(6, 2), System.Globalization.NumberStyles.HexNumber);
      }
      return new Color32(r, g, b, a);
   }

   public static Color intToColor(uint aCol)
    {
        byte b = (byte)((aCol) & 0xFF);
        byte g = (byte)((aCol>>8) & 0xFF);
        byte r = (byte)((aCol>>16) & 0xFF);
        return new Color32(r, g, b, 255);
    }
}
