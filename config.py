# config.py — Word Game Pro Configuration

AGE_GROUPS = {
    "kids":   (0,  10),
    "teens": (11,  16),
    "adults":(17, 120),
}

# Word length range per age × level band (3 bands: lvl 1-3, 4-6, 7-10)
# Designed so level 1 is always comfortable and difficulty climbs smoothly
WORD_LENGTH = {
    "kids":   [(3, 4),  (4, 6),  (5, 8)],
    "teens":  [(3, 5),  (5, 7),  (7, 11)],
    "adults": [(3, 5),  (5, 8),  (8, 15)],
}

def level_band(level):
    if level <= 3: return 0
    if level <= 6: return 1
    return 2

# ── WORD BANKS ───────────────────────────────────────────────────
# Every bank includes COMMON short words at the start (for early levels)
# and progressively harder/longer words for later levels.
# Adults get common everyday words PLUS subject-specific harder words.

WORD_BANKS = {

    # KIDS: 3-8 letters, everyday objects, animals, food, actions
    "kids": [
        # 3-letter animals & nature
        "cat","dog","cow","hen","pig","ant","bee","bat","owl","rat","fox","elk",
        "yak","emu","fly","bug","cub","pup","cub","jay","ram","dam","doe","ewe",
        "asp","gnu","koi",
        # 3-letter objects & actions
        "cup","pot","pan","jug","rug","bin","box","bag","fan","map","pen","hat",
        "bed","car","bus","bat","cap","jar","net","log","rod","rod","web","wax",
        "run","hop","sit","eat","fly","cry","dig","cut","mix","rub","dip","pat",
        "nap","tap","sip","sob","hug","jog","mop","nod","pry","tug","zip",
        # 3-letter food & nature
        "egg","jam","pie","ham","bun","nut","pea","fig","yam","rye","soy","oat",
        "sun","sky","sea","mud","ice","fog","dew","ash","oak","ivy","elm","fir",
        # 4-letter animals
        "frog","toad","bear","deer","wolf","lion","duck","fish","bird","crab",
        "worm","mole","hare","pony","lamb","swan","crow","hawk","moth","slug",
        "snail","mink","lynx","newt","vole","wasp","dove","wren","puma",
        # 4-letter food
        "cake","milk","rice","soup","corn","bean","pear","plum","kiwi","lime",
        "meat","fish","tuna","beef","pork","lamb","salt","herb","mint","sage",
        # 4-letter objects & actions
        "book","door","lamp","bell","drum","flag","doll","kite","boat","ship",
        "rope","lock","bolt","nail","hook","ring","cord","tape","disc","pipe",
        "jump","swim","sing","read","draw","talk","walk","play","open","shut",
        "fold","wrap","fill","pour","boil","bake","cook","chop","peel","wash",
        # 4-letter nature
        "rain","snow","wind","fire","rock","leaf","root","seed","tree","pond",
        "cave","hill","lake","mist","wave","tide","sand","soil","dust","gust",
        # 4-letter colours / school
        "blue","pink","gold","grey","teal","ruby","jade","rose","navy","lime",
        "read","math","book","test","draw","sing","play","work","rest","nap",
        # 5-letter words
        "apple","grape","mango","melon","onion","lemon","peach","bread","cream",
        "horse","tiger","zebra","koala","panda","moose","camel","otter","hyena",
        "gecko","finch","robin","table","chair","clock","brush","towel","spoon",
        "plate","smile","laugh","climb","catch","throw","clean","quiet","brave",
        "happy","funny","cloudy","storm","river","beach","stone","grass","field",
        # 5-letter nature & objects
        "brook","coral","flame","frost","chalk","flute","drums","piano","globe",
        "atlas","compass","torch","plank","wheel","chain","crane","shelf","ledge",
        # 6-letter words (mid difficulty for kids)
        "rabbit","kitten","turtle","monkey","donkey","lizard","parrot","flower",
        "forest","desert","jungle","meadow","pebble","stream","butter","cheese",
        "potato","tomato","banana","cherry","almond","pepper","garlic","ginger",
        "orange","cookie","noodle","crayon","pencil","basket","candle","mirror",
        "window","pillow","blanket","bridge","castle","garden","planet","signal",
        "sunset","breeze","puddle","cactus","bamboo","walnut","muffin","cobweb",
        # 7-8 letter words (late levels for kids)
        "sparrow","dolphin","penguin","cheetah","lobster","hamster","broccoli",
        "spinach","pumpkin","avocado","biscuit","cushion","lantern","bicycle",
        "blanket","cabinet","rainbow","thunder","volcano","starfish","caterpillar",
        "elephant","squirrel","dinosaur","calendar","snowball","birthday",
        "baseball","football","butterfly","sandwich","umbrella","backpack",
    ],

    # TEENS: 3-12 letters — starts easy, gets academic
    "teens": [
        # Short common words (early levels)
        "atom","cell","gene","lens","lava","tide","echo","acid","wave","heat",
        "mass","iron","zinc","myth","riot","plot","rhyme","prose","code","data",
        "site","icon","file","post","link","math","test","book","exam","quiz",
        "race","team","goal","ball","game","rule","plan","idea","fact","note",
        "list","step","part","side","line","form","word","text","view","case",
        # 5-6 letter science & geography
        "orbit","ozone","laser","prism","algae","fungi","virus","nerve","artery",
        "solid","fluid","light","sound","force","power","speed","angle","curve",
        "north","south","river","ocean","coast","plain","ridge","cliff","coral",
        "tropic","desert","island","forest","valley","canyon","tundra","steppe",
        "colony","empire","senate","treaty","revolt","reform","ballot","policy",
        # 5-6 letter literature & maths
        "theme","verse","fable","genre","irony","story","novel","essay","rhyme",
        "prime","chord","graph","proof","range","slope","ratio","digit","angle",
        "logic","proof","axiom","limit","curve","scale","table","chart","model",
        # 6-7 letter words
        "magnet","neutron","photon","plasma","pollen","reflex","retina","sodium",
        "calorie","climate","drought","eclipse","erosion","gravity","hormone",
        "mineral","nucleus","protein","tsunami","vaccine","voltage","algebra",
        "decimal","integer","equation","fraction","geometry","parabola","theorem",
        "dialect","fiction","imagery","narrator","satire","tragedy","allegory",
        "monarch","pilgrim","slavery","suffrage","republic","diplomat","feudal",
        "penalty","referee","stadium","stamina","circuit","defence","tactics",
        "battery","browser","display","network","program","storage","keyboard",
        # 7-9 letter words (mid levels)
        "skeleton","electron","asteroid","bacteria","ecosystem","hibernate",
        "migration","evaporate","photosynthesis","condensation",
        "biography","prologue","epilogue","synopsis","symbolism","flashback",
        "exponent","sequence","variable","calculus","tangent","parabola",
        "democracy","revolution","parliament","citizenship","colonialism",
        "renaissance","enlightenment","independence",
        "marathon","dribble","champion","tournament","percussion","improvise",
        "download","software","hardware","internet","algorithm","encryption",
        # 9-12 letter words (late levels)
        "chromosome","combustion","atmosphere","biodiversity","radioactivity",
        "gravitational","electromagnetic","photosynthesis","conservation",
        "protagonist","antagonist","foreshadowing","alliteration","juxtaposition",
        "probability","trigonometry","permutation","differentiation","integration",
        "parliamentary","sovereignty","totalitarianism",
        "cybersecurity","programming","virtualisation","application",
    ],

    # ADULTS: starts with common 3-5 letter words, builds to complex terms
    "adults": [
        # ── EARLY LEVELS: common 3-5 letter words everyone knows ──
        # 3-letter
        "age","art","aim","aid","ban","bar","cap","car","day","due","ego","era",
        "eye","fee","fit","gap","gut","key","law","lay","map","net","odd","pay",
        "raw","row","set","sum","tax","tip","use","war","way","win","wit","flaw",
        # 4-letter common
        "able","back","base","bold","bond","born","case","cash","cost","deal",
        "debt","deed","done","dose","draw","drop","drug","dual","dull","duty",
        "edge","fact","fail","fair","fall","farm","fast","fate","fear","feel",
        "firm","flag","flat","flaw","fled","flux","fold","fond","food","fool",
        "form","free","fuel","full","fund","gain","game","gave","glad","goal",
        "good","grow","half","hard","harm","hate","heal","heat","held","help",
        "hide","high","hint","hold","hole","home","hope","huge","hunt","idea",
        "idle","join","keen","keep","kind","know","lack","land","last","lead",
        "lean","left","life","like","link","list","live","load","loan","long",
        "look","loop","lose","loss","loud","love","make","mark","mass","meet",
        "mild","mind","miss","mode","move","myth","name","need","news","next",
        "note","null","open","over","pace","pain","part","pass","path","peak",
        "plan","play","plot","poor","port","post","pull","pure","push","race",
        "rage","rank","rate","real","rely","rent","rest","rich","ride","ring",
        "rise","risk","role","root","ruin","rule","rush","safe","same","save",
        "seek","self","sell","send","show","side","sign","site","size","skip",
        "slip","slow","soft","sold","sole","sort","span","spin","spot","step",
        "stop","such","suit","swap","take","talk","task","test","then","thin",
        "thus","time","tiny","told","toll","tone","took","tool","torn","true",
        "turn","type","unit","upon","used","vast","view","void","vote","wage",
        "wake","walk","warn","weak","wide","wild","will","wire","wish","word",
        "work","wrap","year","your","zero","zone","bold","core","dark","deep",
        "even","ever","fair","fall","feel","fine","firm","flow","fly","foul",
        # 5-letter common
        "about","abuse","admit","adopt","adult","after","again","agent","agree",
        "ahead","allow","alone","alter","angle","apart","apply","argue","arise",
        "aside","asset","avoid","aware","badly","basic","basis","begin","being",
        "below","birth","black","blame","blank","blend","block","blood","board",
        "bonus","boost","bound","brain","brand","brave","break","breed","brief",
        "bring","broad","broke","build","built","burst","buyer","carry","catch",
        "cause","cease","chain","chair","chaos","chart","check","chief","child",
        "civil","claim","class","clean","clear","climb","close","coach","coast",
        "count","court","cover","crack","craft","crash","crazy","crime","cross",
        "crowd","curve","cycle","daily","death","delay","depth","dirty","doubt",
        "draft","drain","drama","drawn","dream","drive","dwell","early","earth",
        "eight","elite","empty","enemy","enjoy","enter","entry","equal","error",
        "essay","event","exact","exist","extra","faint","faith","false","fancy",
        "fatal","fault","field","fight","final","first","fixed","flesh","float",
        "floor","focus","force","forge","forth","forum","found","frame","fraud",
        "fresh","front","fully","funny","given","grace","grade","grand","grant",
        "grasp","grave","great","green","gross","group","guard","guide","guilt",
        "heart","heavy","hence","human","ideal","image","imply","index","inner",
        "input","inter","issue","joint","judge","large","later","layer","learn",
        "least","leave","legal","level","light","limit","local","logic","loose",
        "lower","lucky","magic","major","maker","meant","media","mercy","merge",
        "merit","metal","might","minor","mixed","model","money","moral","mount",
        "mouse","mouth","moved","music","naive","never","night","noble","north",
        "occur","offer","often","order","other","outer","owner","panel","paper",
        "party","pause","peace","phone","piece","pilot","pitch","pixel","place",
        "plain","plane","plant","plate","plaza","point","power","press","price",
        "pride","prime","print","prior","prize","proof","proud","prove","queue",
        "quiet","quote","raise","range","rapid","ratio","reach","ready","realm",
        "rebel","refer","reign","relax","reply","right","rigid","rough","round",
        "royal","rural","scene","scope","score","sense","serve","seven","shall",
        "shape","share","sharp","shift","shoot","short","sight","skill","sleep",
        "slide","slope","smart","smile","smoke","solve","sound","south","space",
        "spark","spend","spite","split","spoke","sport","staff","stage","stake",
        "stand","start","state","stays","steal","steel","still","stock","stone",
        "store","storm","story","style","sugar","super","surge","sweep","sweet",
        "swore","table","teach","teeth","tends","terms","theme","thick","thing",
        "think","third","those","three","threw","throw","tight","timer","title",
        "today","token","total","touch","tough","tower","track","trade","trail",
        "train","treat","trend","trial","tribe","trick","tried","trust","truth",
        "twice","under","union","until","upper","urban","usual","value","video",
        "viral","visit","vital","vivid","voice","waste","watch","water","weigh",
        "weird","where","which","while","white","whole","whose","wider","woman",
        "women","world","worse","worst","worth","would","write","wrong","yield",
        "young","youth",
        # ── MID LEVELS: subject-specific 5-8 letter words ──
        "ethics","reason","virtue","dogma","axiom","thesis","trauma","phobia",
        "schema","anxiety","cognition","delusion","empathy","impulse","placebo",
        "verdict","statute","mandate","plaintiff","autonomy","clemency","doctrine",
        "equity","tariff","surplus","deficit","liquidity","monopoly","austerity",
        "entropy","quantum","inertia","isotope","polymer","catalyst","diffusion",
        "facade","baroque","cubism","baroque","balance","harmony","texture",
        "syntax","lexeme","morpheme","phoneme","semiotics","ambiguity","cognate",
        "taboo","totem","ritual","kinship","caste","diaspora","folklore","ideology",
        "budget","invest","profit","export","import","supply","demand","market",
        "treaty","debate","ballot","reform","revolt","census","tenure","clause",
        "memoir","satire","fable","prose","irony","genre","motif","lyric","verse",
        # ── LATE LEVELS: long academic/technical words ──
        "rhetoric","solipsism","syllogism","dialectic","empirical","nihilism",
        "hedonism","stoicism","relativism","pragmatism","rationalism","absurdism",
        "determinism","existential","metaphysics","consciousness","consequentialism",
        "deontological","transcendentalism","phenomenology","epistemology","utilitarianism",
        "narcissism","obsession","paranoia","psychosis","resilience","serotonin",
        "attachment","behaviour","dementia","hallucination","introspection",
        "neuroplasticity","psychoanalysis","schizophrenia","psychotherapy",
        "dissociation","psychosomatic","desensitisation","neurotransmitter",
        "gerrymandering","jurisdiction","totalitarianism","constitution",
        "jurisprudence","prosecutorial","indictment","sovereignty","bureaucracy",
        "mercantilism","privatisation","depreciation","microeconomics","macroeconomics",
        "cryptocurrency","protectionism","hyperinflation","deregulation","equilibrium",
        "thermodynamics","calcification","conductivity","crystallisation",
        "electromagnetic","mitochondria","nanotechnology","bioluminescence",
        "chemosynthesis","bioengineering","superconductor","spectroscopy",
        "impressionism","functionalism","postmodernism","expressionism",
        "juxtaposition","chiaroscuro","ornamentation","neoclassical",
        "onomatopoeia","colloquialism","circumlocution","personification","portmanteau",
        "assimilation","globalisation","marginalisation","socialisation",
        "stratification","urbanisation","intersectionality","postcolonialism",
        "multiculturalism","discrimination","gentrification","radicalisation",
    ],
}

# Strip any accidental multi-word or hyphenated entries
for _grp in WORD_BANKS:
    WORD_BANKS[_grp] = list(dict.fromkeys(
        w.strip() for w in WORD_BANKS[_grp]
        if w.strip() and " " not in w.strip() and "-" not in w.strip()
    ))

# ── LEVEL SETTINGS ───────────────────────────────────────────────
LEVEL_SETTINGS = {
    1:  {"time": 90,  "words": 5,  "points": 10},
    2:  {"time": 110, "words": 8,  "points": 12},
    3:  {"time": 130, "words": 12, "points": 15},
    4:  {"time": 150, "words": 15, "points": 18},
    5:  {"time": 170, "words": 18, "points": 20},
    6:  {"time": 190, "words": 22, "points": 25},
    7:  {"time": 210, "words": 26, "points": 30},
    8:  {"time": 230, "words": 30, "points": 35},
    9:  {"time": 250, "words": 35, "points": 40},
    10: {"time": 270, "words": 40, "points": 50},
}

HINT_COST           = 5
WRONG_GUESS_PENALTY = 2
MAX_LEADERBOARD     = 10
LEADERBOARD_FILE    = "leaderboard.json"