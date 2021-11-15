using System;
using System.Collections.Generic;
using UnityEngine;
using Unity.Entities;
using Unity.Transforms;
using Unity.Rendering;
using Unity.Mathematics;
using Unity.Entities.UniversalDelegates;
using System.Linq;

public class Tree
{
    public int id;
    public int treeId;
    public int scrubId;
    public GameObject existence;
    public bool alive; //tree is consumeable item
    public Vector3 pos;
    public Quaternion rot;
    static private string filepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Trees/";
    static private int numTreePrefabs = 17;
    static private int numScrubPrefabs = 1;
    static private List<Prefab> treePrefabs;
    static private List<Prefab> scrubPrefabs;

    static public void LoadPrefabs()
    {
        treePrefabs = new List<Prefab>();
        for (int i = 0; i < numTreePrefabs; i++)
        {
            treePrefabs.Add(Resources.Load(filepath + "Tree_" + i) as Prefab);
        }
        scrubPrefabs = new List<Prefab>();
        for (int i = 0; i < numScrubPrefabs; i++)
        {
            treePrefabs.Add(Resources.Load(filepath + "Tree_trunk_" + i) as Prefab);
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
        this.existence = Instantiate((this.alive == true ? treePrefabs[this.treeId] : scrubPrefabs[this.scrubId]), pos, rot) as GameObject;
    }

    public void UpdateAliveStatus(bool alive)
    {
        if (this.alive != alive)
        {
            this.alive = alive;
            this.Destroy();
            this.existence = Instantiate((this.alive == true ? treePrefabs[this.treeId] : scrubPrefabs[this.scrubId]), this.pos, this.rot) as GameObject;
        }
    }

    public void Destroy()
    {
        Destroy(this.existence);
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
    static private List<Prefab> stonePrefabs;
    static private string filepath = "tiles_v2/Tiles/Fill parts/Grass/Stone_";
    static private int numScrubPrefabs = 2;
    static public void LoadPrefabs()
    {
        stonePrefabs = new List<Prefab>();
        for (int i = 0; i < numScrubPrefabs; i++)
        {
            stonePrefabs.Add(Resources.Load(filepath + i) as Prefab);
        }
    }

    public Stone(int id, bool status, Vector3 pos, Quaternion rot)
    {
        this.stoneId = Random.Range(0, stonePrefabs.Count);
        this.alive = staus;
        this.pos = pos;
        this.rot = rot;
        this.id = id;  // local id in the tile
        this.existence = (this.alive == true ? Instantiate(stonePrefabs[this.stoneId], pos, rot) as GameObject : null);
    }

    public void UpdateAliveStatus(bool alive)
    {
        if (this.alive != alive)
        {
            this.alive = alive;
            this.Destroy();
            this.existence = (this.alive == true ? Instantiate(stonePrefabs[this.stoneId], pos, rot) as GameObject : null);
        }
    }

    public void Destroy()
    {
        if (this.existence != null)
        {
            Destroy(this.existence);
        }
    }
}

public class Stick
{
    public GameObject existence;
    public bool isSmall;
    static private List<Prefab> stickPrefabs;
    static private string filepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Branchs/Branch_";
    static private int numSmallStickPrefabs = 7;
    static private int numLargeStickPrefabs = 19;
    static public void LoadPrefabs()
    {
        stickPrefabs = new List<Prefab>();
        for (int i = 0; i < numLargeStickPrefabs; i++)
        {
            stickPrefabs.Add(Resources.Load(filepath + i) as Prefab);
        }
    }

    public Stick(bool isSmall, Vector3 pos, Quaternion rot)
    {
        int stickId = (isSmall ? Random.Range(0, numSmallStickPrefabs) : Random.Range(numSmallStickPrefabs, numLargeStickPrefabs));
        this.isSmall = isSmall;
        this.existence = Instantiate(stickPrefabs[stickId], pos, rot) as GameObject;
    }
    public void Destroy()
    {
        Destroy(this.existence);
    }
}

public class Pebble
{
    public GameObject existence;
    public bool isSmall;
    static private List<Prefab> smallPebblePrefabs;
    static private List<Prefab> largePebblePrefabs;
    static private string largePebbleFilepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Stones/Sets/Stones_";
    static private string smallPebbleFilepath = "Low Poly Isometric Tiles - Cartoon Pack/Prefabs/Stones/Stone_";
    static private int numSmallStickPrefabs = 40;
    static private int numLargePebblePrefabs = 2;
    static public void LoadPrefabs()
    {
        largePebblePrefabs = new List<Prefab>();
        for (int i = 0; i < numLargePebblePrefabs; i++)
        {
            largePebblePrefabs.Add(Resources.Load(largePebbleFilepath + i) as Prefab);
        }
        smallPebblePrefabs = new List<Prefab>();
        for (int i = 0; i < numSmallPebblePrefabs; i++)
        {
            smallPebblePrefabs.Add(Resources.Load(smallPebbleFilepath + i) as Prefab);
        }
    }

    public Pebble(bool isSmall, Vector3 pos, Quaternion rot)
    {
        int pebbleId = (isSmall ? Random.Range(0, numSmallPebblePrefabs) : Random.Range(0, numLargePebblePrefabs));
        this.isSmall = isSmall;
        this.existence = Instantiate((isSmall ? smallPebblePrefabs[pebbleId] : largePebblePrefabs[pebbleId]), pos, rot) as GameObject;
    }
    public void Destroy()
    {
        Destroy(this.existence);
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

    static private List<Prefab> topParts;
    static private List<Prefab> mainParts;
    static private List<Prefab> fillParts;
    static private Material water;

    static private int lavaVal = 0;  //legacy
    static private int waterVal = 1;
    static private int grassVal = 2;
    static private int scrubVal = 3;  //dead tree
    static private int forestVal = 4;  //alive tree
    static private int stoneVal = 5;  //alive stone
    static private int brokenStoneVal = 7;
    public int maxSpawnAttemptsPerObstacle = 10;

    static public void LoadTileParts()
    {
        topParts = new List<Prefab>();
        mainParts = new List<Prefab>();
        fillParts = new List<Prefab>();

        string topPathname = "tiles_v2/Tiles/Top parts/Big/Top_Big_0_";
        string mainPathname = "tiles_v2/Tiles/Main parts/Big/Main_Big_0";
        string fillPathname = "tiles_v2/Tiles/Fill parts/Grass/Only Grass/Fill_Grass_";

        //Load top tile parts
        for (int i = 0; i < this.numTopParts; i++)
        {
            this.topParts.Add(Resources.Load(topPathname + i) as Prefab);
        }

        //Load brick tile part
        this.mainParts.Add(Resources.Load(mainPathname) as Prefab);

        //Load fill tile parts, including grass
        for (int i = 0; i < numFillParts; i++)
        {
            this.fillParts.Add(Resources.Load(fillPathname + i) as Prefab);
        }

        //Load water material
        this.water = Resources.Load("Material/Water") as Material;
    }

    public Tile(string name, int val, Vector3 spawnPos)
    {
        this.name = name;
        this.pos = spawnPos;
        this.topId = Random.Range(0, this.topParts.Count);
        this.top = Instantiate(topParts[this.topId], spawnPos, new Quaternion());
        this.mainId = Random.Range(0, mainParts.Count);
        this.main = Instantiate(mainParts[this.mainId], top.transform);
        this.fill = null;

        if (val == grassVal)
        {
            this.fillId = Random.Range(0, fillParts.Count);
            this.fill = Instantiate(fillParts[this.fillId], top.transform);
            if (randomizeFillChilds)
            {
                for (int i = 0; i < fill.transform.childCount; i++)
                {
                    fill.transform.GetChild(i).gameObject.SetActive(Random.Range(0, 2) == 0 ? false : true);
                    if (fill.transform.GetChild(i).gameObject.activeSelf)
                    {
                        if (randomizeChildsRotation)
                        {
                            fill.transform.GetChild(i).localEulerAngles = new Vector3(0, Random.Range(0f, 360f), 0);
                        }
                    }
                    else
                    {
                        toDestroy.Add(fill.transform.GetChild(i).gameObject);
                    }
                }
            }
        }
        else if (val == waterVal)
        {
            this.top.GetComponent<MeshRenderer>().materials[0] = water;
        }
        else if (val == forestVal || val == scrubVal)
        {
            int id = this.trees.Count;
            Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
            this.trees.Add(new Tree(id, val == forestVal, this.getUncollisionedSpawnPos(spawnPos, 0.1f), rot));
        }
        else if (val == stoneVal)
        {
            int id = this.stones.Count;
            Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
            this.stones.Add(new Stone(id, true, this.getUncollisionedSpawnPos(spawnPos, 0.35f), rot));
        }

        this.smallPebbles = new List<Pebble>();
        this.largePebbles = new List<Pebble>();
        this.smallSticks = new List<Stick>();
        this.largeSticks = new List<Stick>();
    }

    public void UpdateStatus(int val)
    {
        if (val == grassVal)
        {
            // remove all trees and stones
            foreach (Tree obj in this.trees)
            {
                obj.Destroy();
                this.trees.RemoveAll();
            }
            foreach (Stone obj in this.stones)
            {
                obj.Destroy();
                this.stones.RemoveAll();
            }

            this.fillId = Random.Range(0, fillParts.Count);
            this.fill = Instantiate(fillParts[this.fillId], top.transform);
            if (randomizeFillChilds)
            {
                for (int i = 0; i < fill.transform.childCount; i++)
                {
                    fill.transform.GetChild(i).gameObject.SetActive(Random.Range(0, 2) == 0 ? false : true);
                    if (fill.transform.GetChild(i).gameObject.activeSelf)
                    {
                        if (randomizeChildsRotation)
                        {
                            fill.transform.GetChild(i).localEulerAngles = new Vector3(0, Random.Range(0f, 360f), 0);
                        }
                    }
                    else
                    {
                        toDestroy.Add(fill.transform.GetChild(i).gameObject);
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
                    obj.UpdateAliveStatus(True);
                    allAlive = false;
                    break;
                }
            }
            if (allAlive)
            {
                int id = this.trees.Count;
                Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
                this.trees.Add(new Tree(id, val == forestVal, this.getUncollisionedSpawnPos(spawnPos, 0.1f), rot));
            }
        }
        else if (val == scrubVal)
        {
            bool allDead = true;
            foreach (Tree obj in this.trees)
            {
                if (obj.alive)
                {
                    obj.UpdateAliveStatus(False);
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
                    obj.UpdateAliveStatus(True);
                    allAlive = false;
                    break;
                }
            }
            if (allAlive)
            {
                int id = this.stones.Count;
                Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
                this.trees.Add(new Tree(id, val == forestVal, this.getUncollisionedSpawnPos(spawnPos, 0.35f), rot));
            }
        }
        else if (val == brokenStoneVal)
        {
            bool allDead = true;
            foreach (Stone obj in this.stones)
            {
                if (obj.alive)
                {
                    obj.UpdateAliveStatus(False);
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


    public void AddSmallPepple(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
            this.smallPebbles.Add(new Pebble(true, this.pos + this.getUncollisionedSpawnPos(this.pos, 0.05f), rot));
        }
    }

    public void RemoveSmallPepple(int num)
    {
        int tot = this.smallPebbles.Count;
        for (int i = 0; i < num; i++)
        {
            this.smallPebbles[tot - i - 1].Destroy();
        }
        this.smallPebbles.RemoveRange(tot - num, num);
    }

    public void AddLargePepple(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
            this.largePebbles.Add(new Pebble(true, this.pos + this.getUncollisionedSpawnPos(this.pos, 0.2f), rot));
        }
    }

    public void RemoveLargePepple(int num)
    {
        int tot = this.largePebbles.Count;
        for (int i = 0; i < num; i++)
        {
            this.largePebbles[tot - i - 1].Destroy();
        }
        this.largePebbles.RemoveRange(tot - num, num);
    }

    public void AddSmallStick(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
            this.smallPebbles.Add(new Pebble(true, this.pos + this.getUncollisionedSpawnPos(this.pos, 0.1f), rot));
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

    public void AddLargeStick(int num)
    {
        for (int i = 0; i < num; i++)
        {
            Quaternion rot = Quaternion.Euler(0.0f, Randon.Range(0.0f, 360.0f), 0.0f);
            this.largeSticks.Add(new Pebble(true, this.pos + this.getUncollisionedSpawnPos(this.pos, 0.2f), rot));  // TODO: Collision check doesnt work on sticks
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
        Destroy(this.top);
        Destroy(this.main);
        if (this.fill != null) { Destroy(this.fill); }
        foreach (Tree obj in this.trees)
        {
            obj.Destroy();
            this.trees.RemoveAll();
        }
        foreach (Stone obj in this.stones)
        {
            obj.Destroy();
            this.stones.RemoveAll();
        }
        foreach (Pebble obj in this.smallPebbles)
        {
            obj.Destroy();
            this.smallPebbles.RemoveAll();
        }
        foreach (Pebble obj in this.largePebbles)
        {
            obj.Destroy();
            this.largePebbles.RemoveAll();
        }
        foreach (Stick obj in this.smallSticks)
        {
            obj.Destroy();
            this.smallSticks.RemoveAll();
        }
        foreach (Stick obj in this.largeSticks)
        {
            obj.Destroy();
            this.largeSticks.RemoveAll();
        }
    }

    private Vector3 getUncollisionedSpawnPos(Vector3 spawnPos, float obstacleCheckRadius)
    {
        Vector3 pos = Vector3.zero;
        bool validPos = false;
        int spawnAttempts = 0;

        while (!validPos && spawnAttempts < maxSpawnAttemptsPerObstacle)
        {
            spawnAttempts++;

            pos = new Vector3(Random.Range(-0.5f, 0.5f), 0, Random.Range(-0.5f, 0.5f));

            validPos = true;

            Collider[] colliders = Physics.OverlapSphere(spanPos + pos, obstacleCheckRadius);
            foreach (Collider col in colliders)
            {
                foreach (GameObject obj in this.stones)
                {
                    validPos = !(col.tag == obj.tag);
                }
                foreach (GameObject obj in this.trees)
                {
                    validPos = !(col.tag == obj.tag);
                }
                foreach (GameObject obj in this.smallPebbles)
                {
                    validPos = !(col.tag == obj.tag);
                }
                foreach (GameObject obj in this.smallSticks)
                {
                    validPos = !(col.tag == obj.tag);
                }
                foreach (GameObject obj in this.largePebbles)
                {
                    validPos = !(col.tag == obj.tag);
                }
                foreach (GameObject obj in this.largeSticks)
                {
                    validPos = !(col.tag == obj.tag);
                }
            }

            if (validPos)
            {
                return spanPos + pos;
            }
        }
        return spanPos + pos;
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

        //this.water = GameObject.Find("Client/Environment/Water");
        //this.lava  = GameObject.Find("Client/Environment/LavaCutout");
        //this.sword = GameObject.Find("HeavySword");
        this.light = GameObject.Find("Client/Light");

        Consts.MAP_SIZE = System.Convert.ToInt32(packet["size"]);
        Consts.BORDER = System.Convert.ToInt32(packet["border"]);

        float sz = Consts.MAP_SIZE - 2 * Consts.BORDER;

        this.values = new Texture2D(Consts.MAP_SIZE, Consts.MAP_SIZE);

        this.water.transform.localScale = new Vector3(0.1f * sz, 1, 0.1f * sz);
        this.water.transform.pos = new Vector3(Consts.MAP_SIZE / 2f - 0.5f, -0.06f, Consts.MAP_SIZE / 2f - 0.5f);
        //this.lava.transform.localScale       = new Vector3(28.416334661354583f*sz, 1, 28.416334661354583f*sz);
        //this.lava.transform.pos         = new Vector3(Consts.MAP_SIZE / 2f - 0.5f, -0.6f, Consts.MAP_SIZE / 2f - 0.5f);
        this.cameraAnchor.transform.pos = new Vector3(Consts.MAP_SIZE / 2f, 0f, Consts.MAP_SIZE / 2f);
        //this.sword.transform.pos        = new Vector3(Consts.MAP_SIZE / 2f, 6f, Consts.MAP_SIZE / 2f);
        this.light.transform.pos = new Vector3(Consts.MAP_SIZE / 2f, 0f, Consts.MAP_SIZE / 2f);


        List<object> map = (List<object>)packet["map"];
        this.tiles = new Dictionary<Tuple<int, int>, Tile>();
        if (this.vals == null)
        {
            this.vals = new int[Consts.MAP_SIZE, Consts.MAP_SIZE];
            Debug.Log("Setting val map");
            for (int r = 0; r < Consts.MAP_SIZE; r++)
            {
                List<object> row = (List<object>)map[r];
                for (int c = 0; c < Consts.MAP_SIZE; c++)
                {
                    this.vals[r, c] = System.Convert.ToInt32(row[c]);
                    Vector3 spawnPos = new Vector3(r, 0, c);  // TODO: FIX?
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
        if (packet.ContainsKey("overlay"))
        {
            Debug.Log("Setting overlay pixel values");
            int count = 0;
            List<object> values = (List<object>)packet["overlay"];
            Color[] pixels = new Color[Consts.MAP_SIZE * Consts.MAP_SIZE];
            for (int r = 0; r < Consts.MAP_SIZE; r++)
            {
                List<object> row = (List<object>)values[r];
                for (int c = 0; c < Consts.MAP_SIZE; c++)
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
        List<object> resourceSS = (List<object>)packet["resourceSmallSticks"];
        for (int i = 0; i < resourceSS.Count; i++)
        {
            List<object> pos = (List<object>)resourceSS[i];
            int r = System.Convert.ToInt32(pos[0]);
            int c = System.Convert.ToInt32(pos[1]);
            int d = System.Convert.ToInt32(pos[2]);
            if (d > 0)
            {
                tiles[Tuple.Create(r, c)].AddSmallStick(d);
            }
            else
            {
                tiles[Tuple.Create(r, c)].RemoveSmallStick(-d);
            }
        }

        List<object> resourceLS = (List<object>)packet["resourceLargeSticks"];
        for (int i = 0; i < resourceLS.Count; i++)
        {
            List<object> pos = (List<object>)resourceLS[i];
            int r = System.Convert.ToInt32(pos[0]);
            int c = System.Convert.ToInt32(pos[1]);
            int d = System.Convert.ToInt32(pos[2]);
            if (d > 0)
            {
                tiles[Tuple.Create(r, c)].AddLargeStick(d);
            }
            else
            {
                tiles[Tuple.Create(r, c)].RemoveLargeStick(-d);
            }
        }

        List<object> resourceSP = (List<object>)packet["resourceSmallPepples"];
        for (int i = 0; i < resourceSP.Count; i++)
        {
            List<object> pos = (List<object>)resourceSP[i];
            int r = System.Convert.ToInt32(pos[0]);
            int c = System.Convert.ToInt32(pos[1]);
            int d = System.Convert.ToInt32(pos[2]);
            if (d > 0)
            {
                tiles[Tuple.Create(r, c)].AddSmallPepple(d);
            }
            else
            {
                tiles[Tuple.Create(r, c)].RemoveSmallPepple(-d);
            }
        }

        List<object> resourceLP = (List<object>)packet["resourceLargePepples"];
        for (int i = 0; i < resourceLP.Count; i++)
        {
            List<object> pos = (List<object>)resourceLS[i];
            int r = System.Convert.ToInt32(pos[0]);
            int c = System.Convert.ToInt32(pos[1]);
            int d = System.Convert.ToInt32(pos[2]);
            if (d > 0)
            {
                tiles[Tuple.Create(r, c)].AddLargePepple(d);
            }
            else
            {
                tiles[Tuple.Create(r, c)].RemoveLargePepple(-d);
            }
        }

        List<object> resourceLP = (List<object>)packet["resourceTerrain"];
        for (int i = 0; i < resourceLP.Count; i++)
        {
            List<object> pos = (List<object>)resourceLS[i];
            int r = System.Convert.ToInt32(pos[0]);
            int c = System.Convert.ToInt32(pos[1]);
            int d = System.Convert.ToInt32(pos[2]);
            tiles[Tuple.Create(r, c)].UpdateStatus(d);
        }


        //Activate resources
        foreach (Tuple<int, int> pos in this.env.inactiveResources.ToList())
        {
            if (!resourceSet.Contains(pos))
            {
                Entity tile = this.env.GetTile(pos.Item1, pos.Item2);
                this.entityManager.SetEnabled(tile, true);
                this.env.inactiveResources.Remove(pos);
            }
        }

        //Inactivate resources
        foreach (Tuple<int, int> pos in resourceSet.ToList())
        {
            if (!this.env.inactiveResources.Contains(pos))
            {
                Entity tile = this.env.GetTile(pos.Item1, pos.Item2);
                this.entityManager.SetEnabled(tile, false);
                this.env.inactiveResources.Add(pos);
            }
        }
    }
}
