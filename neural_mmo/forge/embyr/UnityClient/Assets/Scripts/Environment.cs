// new environment (the original implementation is preserved as legacy at Environment(old) file) | qf, mav
using System;
using System.Collections.Generic;
using UnityEngine;
using Unity.Entities;
using Unity.Transforms;
using Unity.Rendering;
using Unity.Mathematics;
using Unity.Entities.UniversalDelegates;
using System.Linq;
using Random=UnityEngine.Random;

// implements basic items in the map (tree, rocks, ...) and tile that is consisted of three components with items on the top | qf, mav
// possible optimization in runtime: remove the remaining prefabs in resources directory  
public class Tree
{
    public int id;
    public int treeId;
    public int scrubId;
    public GameObject existence;
    public bool alive; // tree is consumeable item
    public Vector3 pos;
    public Quaternion rot;
    static private string filepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Trees/";
    static private int numTreePrefabs = 17;
    static private int numScrubPrefabs = 1;
    static private float treeLocalScale = 0.8f;
    static private List<GameObject> treePrefabs;
    static private List<GameObject> scrubPrefabs;

    static public void LoadPrefabs()
    {
        treePrefabs = new List<GameObject>();
        for (int i = 0; i < numTreePrefabs; i++)
        {
            treePrefabs.Add(Resources.Load(filepath + "Tree_" + i) as GameObject);
            treePrefabs[i].transform.localScale = new Vector3(.5f, .5f, .5f);
        }
        scrubPrefabs = new List<GameObject>();
        for (int i = 0; i < numScrubPrefabs; i++)
        {
            scrubPrefabs.Add(Resources.Load(filepath + "Tree_trunk_" + i) as GameObject);
            scrubPrefabs[i].transform.localScale = new Vector3(.5f, .5f, .5f);
        }
    }

    public Tree(int id, bool status, Vector3 pos, Quaternion rot)
    {
        this.treeId = Random.Range(0, treePrefabs.Count);
        this.scrubId = Random.Range(0, scrubPrefabs.Count);
        this.alive = status;
        this.pos = pos;
        this.rot = rot;
        this.id = id;  // local id in the tile
        this.existence = GameObject.Instantiate((this.alive == true ? treePrefabs[this.treeId] : scrubPrefabs[this.scrubId]), pos, rot) as GameObject;
        this.existence.transform.localScale *= treeLocalScale;
    }

    public void UpdateAliveStatus(bool alive)
    {
        if (this.alive != alive)
        {
            this.alive = alive;
            this.Destroy();
            this.existence = GameObject.Instantiate((this.alive == true ? treePrefabs[this.treeId] : scrubPrefabs[this.scrubId]), this.pos, this.rot) as GameObject;
        }
    }

    public void Destroy()
    {
        GameObject.Destroy(this.existence);
    }

}

public class Stone
{
    public int id; //local in the tile
    public int stoneId;
    public GameObject existence;
    public bool alive;
    public Vector3 pos;
    public Quaternion rot;
    static private List<GameObject> stonePrefabs;
    static private string filepath = "tiles_v2/Tiles/Fill parts/Grass/Stone_";
    static private int numScrubPrefabs = 2;
    static public void LoadPrefabs()
    {
        stonePrefabs = new List<GameObject>();
        for (int i = 0; i < numScrubPrefabs; i++)
        {
            stonePrefabs.Add(Resources.Load(filepath + i) as GameObject);
            stonePrefabs[i].transform.localScale = new Vector3(.4f, .4f, .4f);
        }
    }

    public Stone(int id, bool status, Vector3 pos, Quaternion rot)
    {
        Debug.Log("Adding a stone to env");
        this.stoneId = Random.Range(0, stonePrefabs.Count);
        this.alive = status;
        this.pos = pos;
        this.rot = rot;
        this.id = id;  // local id in the tile
        if (this.alive == true){
            this.existence = GameObject.Instantiate(stonePrefabs[this.stoneId], pos, rot);
        }
        else{
            this.existence = null;
        }      
    }

    public void UpdateAliveStatus(bool alive)
    {
        if (this.alive != alive)
        {
            this.alive = alive;
            this.Destroy();
            this.existence = (this.alive == true ? GameObject.Instantiate(stonePrefabs[this.stoneId], pos, rot) as GameObject : null);
        }
    }

    public void Destroy()
    {
        if (this.existence != null)
        {
            GameObject.Destroy(this.existence);
        }
    }
}

public class Stick
{
    public GameObject existence;
    public bool isSmall;
    static private List<GameObject> stickPrefabs;
    static private string filepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Branchs/Branch_";
    static private int numSmallStickPrefabs = 7;
    static private int numLargeStickPrefabs = 19;
    static public void LoadPrefabs()
    {
        stickPrefabs = new List<GameObject>();
        for (int i = 0; i < numLargeStickPrefabs; i++)
        {
            stickPrefabs.Add(Resources.Load(filepath + i) as GameObject);
            stickPrefabs[i].transform.localScale = new Vector3(.25f, .25f, .25f);;
        }
    }

    public Stick(bool isSmall, Vector3 pos, Quaternion rot)
    {
        int stickId = (isSmall ? Random.Range(0, numSmallStickPrefabs) : Random.Range(numSmallStickPrefabs, numLargeStickPrefabs));
        this.isSmall = isSmall;
        this.existence = GameObject.Instantiate(stickPrefabs[stickId], pos, rot) as GameObject;
    }

    public void Destroy()
    {
        GameObject.Destroy(this.existence);
    }
}

public class Pebble
{
    public GameObject existence;
    public bool isSmall;
    static private List<GameObject> smallPebblePrefabs;
    static private List<GameObject> largePebblePrefabs;
    static private string largePebbleFilepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Stones/Sets/Stones_";
    static private string smallPebbleFilepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Stones/Stone_";
    static private int numSmallPebblePrefabs = 40;
    static private int numLargePebblePrefabs = 2;
    static public void LoadPrefabs()
    {
        largePebblePrefabs = new List<GameObject>();
        for (int i = 0; i < numLargePebblePrefabs; i++)
        {
            largePebblePrefabs.Add(Resources.Load(largePebbleFilepath + i) as GameObject);
            largePebblePrefabs[i].transform.localScale = new Vector3(.25f, .25f, .25f);
        }
        smallPebblePrefabs = new List<GameObject>();
        for (int i = 0; i < numSmallPebblePrefabs; i++)
        {
            smallPebblePrefabs.Add(Resources.Load(smallPebbleFilepath + i) as GameObject);
            smallPebblePrefabs[i].transform.localScale = new Vector3(.25f, .25f, .25f);
        }
    }

    public Pebble(bool isSmall, Vector3 pos, Quaternion rot)
    {
        int pebbleId = (isSmall ? Random.Range(0, numSmallPebblePrefabs) : Random.Range(0, numLargePebblePrefabs));
        this.isSmall = isSmall;
        this.existence =GameObject.Instantiate((isSmall ? smallPebblePrefabs[pebbleId] : largePebblePrefabs[pebbleId]), pos, rot) as GameObject;
    }
    public void Destroy()
    {
        GameObject.Destroy(this.existence);
    }
}

public class Tile
{
    public string name;
    public GameObject top;
    public int topId;
    public GameObject main;
    public int mainId;
    public GameObject fill;
    public int fillId;
    public Vector3 pos;
    public List<Tree> trees;
    public List<Stone> stones;
    public List<Stick> smallSticks;
    public List<Pebble> smallPebbles;
    public List<Stick> largeSticks;
    public List<Pebble> largePebbles;

    private bool randomizeFillChilds = true;

    static private List<GameObject> topParts;
    static private int numTopParts = 7;
    static private List<GameObject> topStoneParts;
    static private int numTopStoneParts = 15;
    static private List<GameObject> mainParts;
    static private List<GameObject> fillParts;
    static private int numFillParts = 9;
    static private Material water;

    static private int lavaVal = 0;  //legacy
    static private int waterVal = 1;
    static private int grassVal = 2;
    static private int scrubVal = 3;  //dead tree
    static private int forestVal = 4;  //alive tree
    static private int stoneVal = 6;  //alive stone
    static private int brokenStoneVal = 5;
    public int maxSpawnAttemptsPerObstacle = 10;

    static private Vector3 magicTree = new Vector3(0, 1f, 0);
    static private Vector3 magicStone = new Vector3(0, 0.13f, 0);
    static private Vector3 magicFill = new Vector3(0, -0.05f, 0);
    static private Vector3 magicResources = new Vector3(0, 0.55f, 0);

    static public void LoadTileParts()
    {
        topParts = new List<GameObject>();
        topStoneParts = new List<GameObject>();
        mainParts = new List<GameObject>();
        fillParts = new List<GameObject>();

        string topPathname = "tiles_v2/Tiles/Top parts/Big/Top_Big_0_";
        string topStonePathname = "tiles_v2/Tiles/Top parts/Stone/Top_Stone_0_"; 
        string mainPathname = "tiles_v2/Tiles/Main parts/Big/Main_Big_0";
        string fillPathname = "tiles_v2/Tiles/Fill parts/Grass/Only Grass/Fill_Grass_";

        //Load top tile parts
        for (int i = 0; i < numTopParts; i++)
        {
            topParts.Add(Resources.Load(topPathname + i) as GameObject);
        }
        for (int i = 0; i < numTopStoneParts; i++)
        {
            topStoneParts.Add(Resources.Load(topStonePathname + i) as GameObject);
        }

        //Load brick tile part
        mainParts.Add(Resources.Load(mainPathname) as GameObject);

        //Load fill tile parts, including grass
        for (int i = 0; i < numFillParts; i++)
        {
            fillParts.Add(Resources.Load(fillPathname + i) as GameObject);
        }

        //Load water material
        water = Resources.Load("Material/Water") as Material;
    }

    int getTileTopId(int val){
        if (val == grassVal){
            return 5; // "Top_Big_0_5"
        }
        else if (val == forestVal){
            return 2;  // "Top_Big_0_2"
        }
        else if (val == scrubVal){  // degenerated forest
            return 0;  // "Top_Big_0_0"
        }
        else if (val == stoneVal){
            return 0;  //Random.Range(0, topStoneParts.Count);
        }
        else{
            return 0;  //Random.Range(0, topParts.Count);
        }
    }

    public Tile(string name, int val, Vector3 spawnPos)
    {
        this.name = name;
        this.pos = spawnPos;
        this.topId = getTileTopId(val);
        GameObject top_temp;
        if (val == stoneVal) {
            top_temp = topStoneParts[this.topId];
        } else {
            top_temp = topParts[this.topId];
        }
        this.top = GameObject.Instantiate(top_temp, spawnPos, new Quaternion());
        this.top.transform.localScale = new Vector3(.5f, .5f, .5f);
        this.mainId = Random.Range(0, mainParts.Count - 1);
        this.main =GameObject.Instantiate(mainParts[this.mainId], this.top.transform);
        this.fill = null;

        this.trees = new List<Tree>();
        this.stones = new List<Stone>();
        this.smallPebbles = new List<Pebble>();
        this.largePebbles = new List<Pebble>();
        this.smallSticks = new List<Stick>();
        this.largeSticks = new List<Stick>();

        if (val == grassVal)
        {
            this.fillId = Random.Range(0, fillParts.Count - 1);
            this.fill =GameObject.Instantiate(fillParts[this.fillId], top.transform);
            this.fill.transform.position += magicFill;
            if (randomizeFillChilds)
            {
                for (int i = 0; i < fill.transform.childCount; i++)
                {
                    fill.transform.GetChild(i).gameObject.SetActive(Random.Range(0, 2) == 0 ? false : true);
                    if (fill.transform.GetChild(i).gameObject.activeSelf)
                    {
                        fill.transform.GetChild(i).localEulerAngles = new Vector3(0, Random.Range(0f, 360f), 0);
                    }
                }
            }
        }
        else if (val == waterVal)
        {
            Debug.Log("Adding water");
            this.top.GetComponent<MeshRenderer>().material = water;
        }
        else if (val == forestVal || val == scrubVal)
        {
            int id = this.trees.Count;
            if (id < 1) {
                Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
                this.trees.Add(new Tree(id, val == forestVal, spawnPos+magicTree, rot));
            }
        }
        else if (val == stoneVal)
        {   
            Debug.Log("making a stone on init");
            int id = this.stones.Count;
            Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
            this.stones.Add(new Stone(id, true, spawnPos+magicStone, rot));
        } else {
            Debug.Log("val didn't find a home: "+val);
        }
    }

    public void UpdateStatus(int val)
    {
        Debug.Log("calling update status with val "+val);
        if (val == grassVal)
        {
            // remove all trees and stones
            foreach (Tree obj in this.trees)
            {
                obj.Destroy();
            }
            this.trees.Clear();
            foreach (Stone obj in this.stones)
            {
                obj.Destroy();
            }
            this.stones.Clear();

            this.fillId = Random.Range(0, fillParts.Count);
            this.fill =GameObject.Instantiate(fillParts[this.fillId], top.transform);
            if (randomizeFillChilds)
            {
                for (int i = 0; i < fill.transform.childCount; i++)
                {
                    fill.transform.GetChild(i).gameObject.SetActive(Random.Range(0, 2) == 0 ? false : true);
                    if (fill.transform.GetChild(i).gameObject.activeSelf)
                    {
                        fill.transform.GetChild(i).localEulerAngles = new Vector3(0, Random.Range(0f, 360f), 0);
                    }
                }
            }
        }
        else if (val == waterVal)
        {
            Debug.Log("WARN: backend is trying to update land to water, ignored.");
        }
        else if (val == forestVal)
        {
            bool allAlive = true;
            foreach (Tree obj in this.trees)
            {
                if (!obj.alive)
                {
                    obj.UpdateAliveStatus(true);
                    allAlive = false;
                    break;
                }
            }
            if (allAlive)
            {
                int id = this.trees.Count;
                if (id < 1) {
                    Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
                    this.trees.Add(new Tree(id, val == forestVal, this.pos+magicTree, rot));
                }
            }
        }
        else if (val == scrubVal)
        {
            bool allDead = true;
            foreach (Tree obj in this.trees)
            {
                if (obj.alive)
                {
                    obj.UpdateAliveStatus(false);
                    allDead = false;
                    break;
                }
            }
            if (allDead)
            {
                Debug.Log("WARN: backend is trying to grow a dead tree, ignored.");
            }
        }
        else if (val == stoneVal)
        {
            bool allAlive = true;
            foreach (Stone obj in this.stones)
            {
                if (!obj.alive)
                {
                    obj.UpdateAliveStatus(true);
                    allAlive = false;
                    break;
                }
            }
            if (allAlive)
            {
                int id = this.stones.Count; //fixme should be stone below?
                Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
                // this.stones.Add(new Stone(id, val == stoneVal, this.pos+magicStone, rot));
            }
        }
        else if (val == brokenStoneVal)
        {
            bool allDead = true;
            foreach (Stone obj in this.stones)
            {
                if (obj.alive)
                {
                    obj.UpdateAliveStatus(false);
                    allDead = false;
                    break;
                }
            }
            if (allDead)
            {
                Debug.Log("WARN: backend is trying to grow a dead stone, ignored.");
            }
        }
    }

    public void SetSmallPebble(int num){
        int delta = num - this.smallPebbles.Count;
        if (delta > 0){
            this.AddSmallPebble(delta);
        }
        else{
            this.RemoveSmallPebble(-delta);
        }
    }

    public void AddSmallPebble(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
            this.smallPebbles.Add(new Pebble(true, this.getUncollisionedSpawnPos(this.pos+magicResources, 0.05f), rot));
        }
    }

    public void RemoveSmallPebble(int num)
    {
        int tot = this.smallPebbles.Count;
        for (int i = 0; i < num; i++)
        {
            this.smallPebbles[tot - i - 1].Destroy();
        }
        this.smallPebbles.RemoveRange(tot - num, num);
    }

    public void SetLargePebble(int num){
        int delta = num - this.largePebbles.Count;
        if (delta > 0){
            this.AddLargePebble(delta);
        }
        else{
            this.RemoveLargePebble(-delta);
        }
    }

    public void AddLargePebble(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
            this.largePebbles.Add(new Pebble(true, this.getUncollisionedSpawnPos(this.pos+magicResources, 0.2f), rot));
        }
    }

    public void RemoveLargePebble(int num)
    {
        int tot = this.largePebbles.Count;
        for (int i = 0; i < num; i++)
        {
            this.largePebbles[tot - i - 1].Destroy();
        }
        this.largePebbles.RemoveRange(tot - num, num);
    }
    
    public void SetSmallStick(int num){
        int delta = num - this.smallSticks.Count;
        if (delta > 0){
            this.AddSmallStick(delta);
        }
        else{
            this.RemoveSmallStick(-delta);
        }
    }
    
    public void AddSmallStick(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
            this.smallSticks.Add(new Stick(true, this.getUncollisionedSpawnPos(this.pos+magicResources, 0.1f), rot));
        }
    }

    public void RemoveSmallStick(int num)
    {
        int tot = this.smallSticks.Count;
        for (int i = 0; i < num; i++)
        {
            this.smallSticks[tot - i - 1].Destroy();
        }
        this.smallSticks.RemoveRange(tot - num, num);
    }

    public void SetLargeStick(int num){
        int delta = num - this.largeSticks.Count;
        if (delta > 0){
            this.AddLargeStick(delta);
        }
        else{
            this.RemoveLargeStick(-delta);
        }
    }
    
    public void AddLargeStick(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Random.Range(0.0f, 360.0f), 0.0f);
            this.largeSticks.Add(new Stick(true, this.getUncollisionedSpawnPos(this.pos+magicResources, 0.2f), rot));  // TODO: Collision check doesnt work on sticks
        }
    }

    public void RemoveLargeStick(int num)
    {
        int tot = this.largeSticks.Count;
        for (int i = 0; i < num; i++)
        {
            this.largeSticks[tot - i - 1].Destroy();
        }
        this.largeSticks.RemoveRange(tot - num, num);
    }

    public void DestroyTile()
    {
        GameObject.Destroy(this.top);
        GameObject.Destroy(this.main);
        if (this.fill != null) { 
            GameObject.Destroy(this.fill); 
        }
        foreach (Tree obj in this.trees)
        {
            obj.Destroy();
        }
        this.trees.Clear();
        foreach (Stone obj in this.stones)
        {
            obj.Destroy();
        }
        this.stones.Clear();
        foreach (Pebble obj in this.smallPebbles)
        {
            obj.Destroy();
        }
        this.smallPebbles.Clear();
        foreach (Pebble obj in this.largePebbles)
        {
            obj.Destroy();
        }
        this.largePebbles.Clear();
        foreach (Stick obj in this.smallSticks)
        {
            obj.Destroy();
        }
        this.smallSticks.Clear();
        foreach (Stick obj in this.largeSticks)
        {
            obj.Destroy();
        }
        this.largeSticks.Clear();
    }

    private Vector3 getUncollisionedSpawnPos(Vector3 spawnPos, float obstacleCheckRadius)
    {
        Vector3 pos = Vector3.zero;
        bool validPos = false;
        int spawnAttempts = 0;

        // return spawnPos;

        while (!validPos && spawnAttempts < maxSpawnAttemptsPerObstacle)
        {
            spawnAttempts++;

            pos = new Vector3(Random.Range(-.25f, .25f), 0, Random.Range(-.25f, .25f));  // not sure if cover tile

            validPos = true;

            Collider[] colliders = Physics.OverlapSphere(spawnPos + pos, obstacleCheckRadius);
            foreach (Collider col in colliders)
            {
                foreach (Stone obj in this.stones)
                {
                    validPos = !(col.tag == obj.existence.tag);
                }
                foreach (Tree obj in this.trees)
                {
                    validPos = !(col.tag == obj.existence.tag);
                }
                foreach (Pebble obj in this.smallPebbles)
                {
                    validPos = !(col.tag == obj.existence.tag);
                }
                foreach (Stick obj in this.smallSticks)
                {
                    validPos = !(col.tag == obj.existence.tag);
                }
                foreach (Pebble obj in this.largePebbles)
                {
                    validPos = !(col.tag == obj.existence.tag);
                }
                foreach (Stick obj in this.largeSticks)
                {
                    validPos = !(col.tag == obj.existence.tag);
                }
            }

            if (validPos)
            {
                return spawnPos + pos;
            }
        }
        return spawnPos + pos;
    }

}

[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
public class Environment : MonoBehaviour
{
    //public static Dictionary<int, Texture2D> tiles   = new Dictionary<int, Texture2D>();
    GameObject root;
    GameObject cameraAnchor;
    GameObject orbitCamera;

    //assembling parts for terrain

    public int[,] vals;
    public Texture2D values;
    Dictionary<string, object> overlays;
    int overlayR;
    int overlayC;
    bool init = false;

    public Dictionary<Tuple<int, int>, Tile> tiles;

    public static List<List<GameObject>> terrain = new List<List<GameObject>>();
    public int[,] oldPacket = new int[Consts.MAP_SIZE, Consts.MAP_SIZE];
    public GameObject[,] objs = new GameObject[Consts.MAP_SIZE, Consts.MAP_SIZE];

    public int tick = 0;
    public bool cmd = false;

    Shader shader;

    GameObject resources;
    GameObject water;
    GameObject light;
    Console console;

    bool first = true;

    Material overlayMatl;

    MeshRenderer renderer;

    bool test = false; // for local testing (allows frontend not to listen's backend's packet)

    private void loadResources()
    {
        Tree.LoadPrefabs();
        Stone.LoadPrefabs();
        Stick.LoadPrefabs();
        Pebble.LoadPrefabs();
        Tile.LoadTileParts();
    }

    public void initTerrain(Dictionary<string, object> packet)
    {
        this.root = GameObject.Find("Environment/Terrain");
        this.resources = GameObject.Find("Client/Environment/Terrain/Resources");

        this.loadResources();

        this.console = GameObject.Find("Console").GetComponent<Console>();
        this.shader = Shader.Find("Standard");

        this.cameraAnchor = GameObject.Find("CameraAnchor");
        this.orbitCamera = GameObject.Find("CameraAnchor/OrbitCamera");

        this.overlayMatl = Resources.Load("Prefabs/Tiles/OverlayMaterial") as Material;
        this.overlayMatl.SetTexture("_Overlay", Texture2D.blackTexture);

        this.water = GameObject.Find("Client/Environment/Water");
        this.light = GameObject.Find("Client/Light");

        Consts.MAP_SIZE = System.Convert.ToInt32(packet["size"]);
        Consts.BORDER = System.Convert.ToInt32(packet["border"]);

        int mapSize = this.test == true? 15: Consts.MAP_SIZE;
        int mapBorder = this.test == true? 1: Consts.BORDER;
        float sz = mapSize - 2 * mapBorder;

        this.values = new Texture2D(mapSize, mapSize);

        this.water.transform.localScale = new Vector3(0.1f * sz, 1, 0.1f * sz);
        this.water.transform.position = new Vector3(Consts.MAP_SIZE / 2f - 0.5f, -0.06f, Consts.MAP_SIZE / 2f - 0.5f);
        this.cameraAnchor.transform.position = new Vector3( mapSize / 2f, 0f,  mapSize / 2f);

        List<object> map = (List<object>)packet["map"];
        this.tiles = new Dictionary<Tuple<int, int>, Tile>();
        
        if (this.vals == null)
        {
            this.vals = new int[mapSize, mapSize];
            Debug.Log("Setting val map");
            float tilesize = 1f; //Consts.TILE_RADIUS()/4;
            for (int r = mapBorder; r < mapSize - mapBorder + 1; r++)
            {
                List<object> row = this.test == true? null : (List<object>)map[r];
                for (int c = mapBorder; c < mapSize - mapBorder + 1; c++)
                {
                    this.vals[r, c] = System.Convert.ToInt32(this.test == true? Random.Range(1, 6): row[c]);
                    Vector3 spawnPos = new Vector3(tilesize*r, -tilesize/2, tilesize*c);  // TODO: FIX?
                    // creates tile
                    tiles.Add(Tuple.Create(r, c), new Tile(r + "_" + c, this.vals[r, c], spawnPos));
                }
            }
        }
        this.init = true;
    }

    public void UpdateMap(Dictionary<string, object> packet)
    {
        GameObject root = GameObject.Find("Environment");
        //this.overlayMatl.SetTexture("_Overlay", Texture2D.blackTexture);
        int mapSize = this.test == true? 15: Consts.MAP_SIZE;
        int mapBorder = this.test == true? 1: Consts.BORDER;

        if (packet.ContainsKey("overlay"))
        {
            Debug.Log("Setting overlay pixel values");
            int count = 0;
            List<object> values = (List<object>)packet["overlay"];
            Color[] pixels = new Color[mapSize * mapSize];
            for (int r = 0; r < mapSize; r++)
            {
                List<object> row = (List<object>)values[r];
                for (int c = 0; c < mapSize; c++)
                {
                    List<object> col = (List<object>)row[c];
                    Color value = new Color();
                    for (int i = 0; i < 3; i++)
                    {
                        value[i] = System.Convert.ToSingle(col[i]);
                    }
                    value.a = 0f;
                    pixels[count] = value;
                    count++;
                }
            }
            this.values.SetPixels(pixels);
            this.values.Apply(false);
            this.cmd = true;
        }

        //Parse inactive resource set
        List<object> resourceSS = this.test == true? null : (List<object>)packet["resourceSmallSticks"];
        int cnt = this.test == true? 5 : resourceSS.Count;
        for (int i = 0; i < cnt; i++)
        {
            List<object> pos = this.test == true? null : (List<object>)resourceSS[i];
            int r = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[0]);
            int c = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[1]);
            int d = this.test == true? Random.Range(1, 5) : System.Convert.ToInt32(pos[2]);
            tiles[Tuple.Create(r, c)].SetSmallStick(d);
        }

        List<object> resourceLS = this.test == true? null : (List<object>)packet["resourceLargeSticks"];
        cnt = this.test == true? 5 : resourceLS.Count;
        for (int i = 0; i < cnt; i++)
        {
            List<object> pos =this.test == true? null : (List<object>)resourceLS[i];
            int r = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[0]);
            int c = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[1]);
            int d = this.test == true? Random.Range(1, 5) : System.Convert.ToInt32(pos[2]);
            tiles[Tuple.Create(r, c)].SetLargeStick(d);
        }

        List<object> resourceSP = this.test == true? null : (List<object>)packet["resourceSmallPebbles"];
        cnt = this.test == true? 5 : resourceSP.Count;
        for (int i = 0; i < cnt; i++)
        {
            List<object> pos = this.test == true? null : (List<object>)resourceSP[i];
            int r = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[0]);
            int c = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[1]);
            int d = this.test == true? Random.Range(1, 5) : System.Convert.ToInt32(pos[2]);
            tiles[Tuple.Create(r, c)].SetSmallPebble(d);
        }

        List<object> resourceLP = this.test == true? null : (List<object>)packet["resourceLargePebbles"];
        cnt = this.test == true? 5 : resourceLP.Count;
        for (int i = 0; i < cnt; i++)
        {
            List<object> pos = this.test == true? null : (List<object>)resourceLS[i];
            int r = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[0]);
            int c = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[1]);
            int d = this.test == true? Random.Range(1, 5) : System.Convert.ToInt32(pos[2]);
            tiles[Tuple.Create(r, c)].SetLargePebble(d);
        }

        List<object> resourceT = this.test == true? null : (List<object>)packet["resourceTerrain"];
        cnt = this.test == true? 2 : resourceT.Count;
        for (int i = 0; i < cnt; i++)
        {
            List<object> pos = this.test == true? null : (List<object>)resourceT[i];
            int r = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[0]);
            int c = this.test == true? Random.Range(1, mapSize-2) : System.Convert.ToInt32(pos[1]);
            int d = this.test == true? Random.Range(1, 5) : System.Convert.ToInt32(pos[2]);
            tiles[Tuple.Create(r, c)].UpdateStatus(d);
        }
    }
    
    void Update()
    {
      if (this.overlayMatl)  // future TODO: accomodate overlay generation with the new environment.
      {
         if (this.cmd)
         {
            Debug.Log("Setting overlay texture");
            this.overlayMatl.SetTexture("_Overlay", this.values);
            this.cmd = false;
         }
         // this.overlayMatl.SetVector("_PanParams", new Vector4(cameraR*Consts.CHUNK_SIZE(), cameraC*Consts.CHUNK_SIZE(), this.overlayR, this.overlayC));
         this.overlayMatl.SetVector("_SizeParams", new Vector4(Consts.TILE_RADIUS(), 0, 0, 0));
      }
    }

}
