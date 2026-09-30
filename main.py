import sys
import json
import os
import yaml
import re
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QInputDialog, QFileDialog, QSizePolicy, QWidget, QDialog, QVBoxLayout, QTextEdit, QHeaderView,QSpinBox,QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, QObject,QTimer
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QMessageBox
)

from char import Ui_HisMajestyTheWorm

APP_DIR = Path(__file__).resolve().parent


from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class MasterySpinBox(QSpinBox):

    def textFromValue(self, value):
        if value == 7:
            return "Mastered"

        return str(value)


class spell():
     def __init__(self,name,realm,component,desc):
          self.name = name
          self.realm = realm
          self.component = component
          self.desc = desc

class bond():
    def __init__(self,guildmate,bond,charged):
        super().__init__()
        self.guildmate = guildmate
        self.bond = bond
        self.charged = charged
    def to_dict(self):
        json_dict = {}
        json_dict["guildmate"] = self.guildmate
        json_dict["bond"] = self.bond
        json_dict["charged"] = self.charged
        return json_dict


class item():
    def __init__(self,name,notches_max,notches_used,flickers_max,flickers_used,lit,charged,worn_belt_slots,two_handed,oversized,desc=""):
            super().__init__()
            self.name = name
            self.notches_max = notches_max
            self.notches_used = notches_used
            self.flickers_max = flickers_max
            self.flickers_used = flickers_used
            self.lit = lit
            self.charged = charged
            self.worn_belt_slots = worn_belt_slots
            self.two_handed = two_handed
            self.oversized = oversized
            self.desc = desc

    def to_dict(self):
        json_dict = {}
        json_dict["name"] = self.name
        json_dict["notches_max"] = self.notches_max
        json_dict["notches_used"] = self.notches_used
        json_dict["flickers_max"] = self.flickers_max
        json_dict["charged"] = self.charged
        json_dict["worn_belt_slots"] = self.worn_belt_slots
        json_dict["two_handed"] = self.two_handed
        json_dict["oversized"] = self.oversized
        json_dict["desc"] = self.desc
        return json_dict


class race():
    def __init__(self,kith,kin,kin_talent,arete_talent):
                 super().__init__()
                 self.kin = kin
                 self.kith = kith
                 self.kin_talent = kin_talent
                 self.arete_talent = arete_talent
    def to_dict(self):
        json_dict = {}
        json_dict["kin"] = self.kin
        json_dict["kith"] = self.kith
        json_dict["kin_talent"] = self.kin_talent
        json_dict["arete_talent"] = self.arete_talent
        return json_dict

class talent():
    def __init__(self,name,desc,xp=0,wounded=False):
                 super().__init__()
                 self.name = name
                 self.desc = desc
                 self.xp = xp
                 self.wounded = wounded
    def to_dict(self):
        json_dict = {}
        json_dict["name"] = self.name
        json_dict["desc"] = self.desc
        json_dict["xp"] = self.xp
        json_dict["wounded"] = self.wounded
        return json_dict
class character():

     status = ["Hale","Staggered","Injured","Death's Door"]
     def __init__(self,name,path,kith,kin,swords,pentacles,cups,wands,quest,arete_tasks,motifs,languages,bonds):
                 super().__init__()
                 self.name = name
                 self.path = path
                 self.kith = kith
                 self.kin = kin
                 self.swords = swords
                 self.pentacles = pentacles
                 self.cups = cups
                 self.wands = wands
                 self.quest = quest
                 self.arete_tasks = arete_tasks
                 self.motifs = motifs
                 self.languages = languages
                 self.bonds = bonds
                 self.human = race("Human","",talent("Proud and Ancient",'''Describe or draw the sigil of your house. Write the
motto of your house.
When your house sigil or motto is dramatically
appropriate for an action being attempted, you test fate
with favor.
Additionally, during Challenges, you may spend a
Resolve and use the Speak Incantation action to cry your
motto aloud. You—and all members of your house that
hear your war cry—gain favor on their next action.''',0,False),talent("Byname",'''You are given a byname, like “the Tall,” “the Corpsegrinder, “the Patron Saint
of Pilgrims,” or “the Blackhearted.” When that byname would be relevant to a
test of fate, similar to a motif, you test with favor.''',0,False))
                 self.high_elf = race("Fay","High Elf",talent("Read the Past",'''All high elves have eidetic memories. Bid lore to
accurately recall anything you have ever seen or heard.
You can go back and count the beads of sweat on your
mother's forehead on the day of your birth, if you wish.''',0,False),talent("Akashic Consiousness",'''Some high elves can cast their memories back through
their bloodlines and ask questions of their ancestors or
past incarnations. Spend a Resolve and ask the GM any
question about an event that happened in the past. If it’s
at all possible that one of your ancestors would know
about it, the GM will answer the question.''',0,False))
                 self.dark_elf = race("Fay","Dark Elf",talent("Foretell",'''Bid lore to ask the GM: “If I do X, will Y happen?”
You receive a “yes” or “no” answer in the form of a
prophetic hunch''',0,False),talent("Spout Doom",'''Spend a Resolve to ask the GM: “If I do X, what will
happen?” The GM provides a prophecy, which pours
unbidden out of your mouth.''',0,False))
                 self.wood_elf = race("Fay","Wood Elf",talent("Keen Senses",'''Wood elves have the eyes of a hawk and the nose of
a wolf. A wood elf ’s senses can grow so acute that
they can hear the chatter of living stone, the gossip of
growing roots, or the rumors of passing insects. Bid
lore to temporarily sharpen one of your senses beyond
normal limits and ask the GM a question based on these
heightened senses. Example questions might include:
• “If I focus my sight, can I read their lips from here?”
• “If I listen very closely, can I tell if anybody is invisible
here? Like, do I hear anybody breathing or any
heartbeats or anything?”
• “I take a tiny taste and spit it back out. Can I tell if
it’s poisoned?”
• “Based on their scent, can I tell which path the thief
went down?”
This ability only lasts a moment. As normal, if the GM
does not give you any new information, you do not
expend a lore bid.''',0,False),talent("Area Sense",'''Spend 2 Resolve to meditate for a watch (p. 90). Draw
a card. The GM describes a number of interesting
“visions” equal to the value of the drawn card during
your meditation. (Remember, pages have a value of 11,
knights have a value of 12, etc.)
These visions are sensual experiences. For example, you
could hear the clatter of dice as bored crusaders gamble,
smell a nearby goblin taking a shit, hear two guards
talking about who’s going to be on duty tonight, sense
the quivering tension of a spike trap embedded in the
ceiling, and so on.
The GM provides these details by looking at their map
and Meatgrinder table. Starting near the player’s current
area and moving outwards, the GM provides one salient
detail from the nearby rooms. Each vision should yield
a meaningful detail (e.g., the presence of a hidden door,
detected by an imperceptible draft in a nearby room),
but need not be elaborate or detailed (i.e., the GM
need not mention that the door is trapped, or that it is
activated by pulling on a statue’s arm).
Any Meatgrinder events that occur when a watch passes
are resolved after the GM has given your visions.''',0,False))
                 self.gnome = race("Fay","Gnome",talent("Weird, Wise, Ancient",'''When you bid lore, you can ask a follow-up question to
the answer for free.''',0,False),talent("Uncanny Knowledge",'''If nobody at the table has an appropriate motif to bid
lore about a subject, you may bid lore about the issue at
hand. This is similar to having a motif of “Whatever You
Don’t Know, I Know.”.''',0,False))
                 self.dwarf = race("Underfolk","Dwarf",talent("Labor Unending",'''You may mark the Stressed condition to stay awake all
night and perform two Camp Actions instead of one; see
page 137 for details on Camp Actions.''',0,False),talent("Iron Beards",'''Spend a Resolve to automatically succeed on a test of
fate related to strength, endurance, or stubbornness.''',0,False))
                 self.halfling = race("Underfolk","Halfling",talent("Hale and Hearty",'''If you eat two rations instead of one during step 2 of the
Camping Phase, you may charge an uncharged Bond.''',0,False),talent("Underfoot",'''Spend a Resolve to automatically succeed on a test of
fate related to being quiet or subtle.''',0,False))
                 self.troll = race("Underfolk","Troll",talent("Giant’s Strength",'''You automatically win contests related to raw strength
(arm wrestling, lifting contests, etc.) against other non-
troll kin.''',0,False),talent("Colossal",'''Some trolls can perform feats of incredible strength that
go beyond what would normally be attempted. Spend a
Resolve to pull a portcullis up, smash down a door, push
down a supporting column, or perform some other feat
of impressive destruction. This talent can’t be used to do
additional damage or give an effect, but can be used to
change the battlefield during a Challenge.''',0,False))  
                 self.earthblood = race("Orc","Earthblood",talent("Quicksilver Blood",'''Your blood has the appearance and consistency of
quicksilver, and is incredibly caustic to metal. When
this talent is Wounded by a metal weapon, the weapon
is Destroyed.''',0,False),talent("Jarl",'''You may hatch or gather a horde of goblins to your
cause. Goblins are pretty independent little creatures.
They see you as “da boss” and take commands from you,
but follow those commands in their own, strange, simple
little ways.
Assembling a goblin horde is a City Action. Spend any
amount of XP to attract 2 + X goblins, where X equals
the amount of XP you spent on this action. You may
only ever have up to 8 goblins in your horde.
A goblin horde counts as an animal companion. No
matter how many goblins are in the horde, they always
count as “one creature” and move around together.
Goblins understand whatever language you speak,
but can only follow one-word commands during
Challenges (given using the Command action). They
have tiny minds.
Every time a goblin horde takes a Wound, one of its
members is killed.
A goblin horde carries or hunts for their own food and
supplies their own gear. Their gear is crap; they do not
have any items or tools that you can use. They can act as
porters: For each goblin in the horde, they can carry one
slot worth of items.''',0,False))            
                 self.seablood = race("Orc","Seablood",talent("Poison Blood",'''Your black blood is a deadly poison. When this talent
is Wounded by a bite, the attacker suffers Critical
damage (p. 125)''',0,False),talent("Jarl",'''You may hatch or gather a horde of goblins to your
cause. Goblins are pretty independent little creatures.
They see you as “da boss” and take commands from you,
but follow those commands in their own, strange, simple
little ways.
Assembling a goblin horde is a City Action. Spend any
amount of XP to attract 2 + X goblins, where X equals
the amount of XP you spent on this action. You may
only ever have up to 8 goblins in your horde.
A goblin horde counts as an animal companion. No
matter how many goblins are in the horde, they always
count as “one creature” and move around together.
Goblins understand whatever language you speak,
but can only follow one-word commands during
Challenges (given using the Command action). They
have tiny minds.
Every time a goblin horde takes a Wound, one of its
members is killed.
A goblin horde carries or hunts for their own food and
supplies their own gear. Their gear is crap; they do not
have any items or tools that you can use. They can act as
porters: For each goblin in the horde, they can carry one
slot worth of items.''',0,False))
                 self.stormblood = race("Orc","Stormblood",talent("Blur",'''Your blood smokes like a thick mist. When this talent
is Wounded, you become Shrouded. This lasts long
enough for you to perform a single action or indefinitely
if you stay still and take no actions.''',0,False),talent("Jarl",'''You may hatch or gather a horde of goblins to your
cause. Goblins are pretty independent little creatures.
They see you as “da boss” and take commands from you,
but follow those commands in their own, strange, simple
little ways.
Assembling a goblin horde is a City Action. Spend any
amount of XP to attract 2 + X goblins, where X equals
the amount of XP you spent on this action. You may
only ever have up to 8 goblins in your horde.
A goblin horde counts as an animal companion. No
matter how many goblins are in the horde, they always
count as “one creature” and move around together.
Goblins understand whatever language you speak,
but can only follow one-word commands during
Challenges (given using the Command action). They
have tiny minds.
Every time a goblin horde takes a Wound, one of its
members is killed.
A goblin horde carries or hunts for their own food and
supplies their own gear. Their gear is crap; they do not
have any items or tools that you can use. They can act as
porters: For each goblin in the horde, they can carry one
slot worth of items.''',0,False))        
                 self.fireblood = race("Orc","Fireblood",talent("Berserkergang",'''Your blood is boiling hot. When this talent is Wounded,
you may choose to enter a berserker rage. While berserk
during a Challenge, you cannot Avoid, Dodge, Speak
Incantations, Banter, or Aid Another; however, all of
your Attacks are made with favor.
Your rage ends when you defeat every enemy on the
field. If an ally has attacked or hurt you during this
Challenge, they count as an enemy. You must spend a
Resolve to end your rage prematurely.''',0,False),talent("Jarl",'''You may hatch or gather a horde of goblins to your
cause. Goblins are pretty independent little creatures.
They see you as “da boss” and take commands from you,
but follow those commands in their own, strange, simple
little ways.
Assembling a goblin horde is a City Action. Spend any
amount of XP to attract 2 + X goblins, where X equals
the amount of XP you spent on this action. You may
only ever have up to 8 goblins in your horde.
A goblin horde counts as an animal companion. No
matter how many goblins are in the horde, they always
count as “one creature” and move around together.
Goblins understand whatever language you speak,
but can only follow one-word commands during
Challenges (given using the Command action). They
have tiny minds.
Every time a goblin horde takes a Wound, one of its
members is killed.
A goblin horde carries or hunts for their own food and
supplies their own gear. Their gear is crap; they do not
have any items or tools that you can use. They can act as
porters: For each goblin in the horde, they can carry one
slot worth of items.''',0,False))        
                 self.kithkin = self.human
                 self.swords_talents = []
                 self.swords_talents.append(talent("Aegis",'''If you are carrying an intact shield and would suffer an
effect from a physical source (an attack, a trap, etc.),
you may elect to Notch your shield instead of taking
the effect.''',0,False))
                 self.swords_talents.append(talent("Doom Eye",'''When wielding a missile weapon during a Challenge,
you may spend a Sword card on your turn to perform a
perfect shot. This Attack automatically hits, regardless
of the target’s Initiative.''',0,False))
                 self.swords_talents.append(talent("Heavy Metal Machine",'''During Challenges, if you are wearing iron or steel
armor, you may use a miscellaneous action (discarding
any card) to add your Swords to your Initiative as an
interrupt against a single action. You may only use this
talent once per round.''',0,False))
                 self.swords_talents.append(talent("Monster Hunter",'''When you master or train this talent, choose both a hated
foe and a specialization of that enemy.
• You gain a motif called “[Foe] Hunter.” You can use
this motif to bid lore about these creatures or to gain
favor in tests of fate related to them, as normal.
• You make Attacks with favor against foes of your
specialization.
Choose a foe and a specialization from the following
list—you can change your foe as a City Action if some new
type of creature really gives you reason to be pissed off.
Beast Hunter
You specialize in hunting, tracking, and trapping beasts
of all shapes and sizes. What qualifies as a “beast”? Well,
if it’s in a medieval bestiary, it’s probably a beast. Beasts
are native to the realm of Flesh—they feast, fight, flee,
and fuck.
Specializations: Any specific species (e.g., bats,
centipedes, chimeras, cockatrices, dinosaurs, tigers)
Elemental Hunter
Your focus is dealing with supernatural embodiments
of nature.
Specializations: Any specific creature (e.g., undine,
salamander, siren, dryad, tree giants)
Man Hunter
You specialize in the most dangerous game. The term
“man” is a bit of a misnomer. This category covers all
kith, kin, and genders.
Specializations: Any specific kith: fay, humans,
underfolk, orcs
Spirit Hunter
Your focus is on alien intelligences from the far realms.
You can deal with incorporeal spirits, manifested spirits,
and possessing spirits.
Specializations: Spirits from one of the far realms (i.e.,
Wastes, Weald, Weird, Welkin)
Undead Hunter
You have experience pacifying the unquiet dead.
Specializations: A specific undead type (e.g., skeleton,
zombie, wraith)
Witch Hunter
If the answer to the question “what is that thing?” is
“a wizard did it,” you can deal with it.
Specializations: Any specific type of magical
manifestation (e.g., beastmen, golems, oozes)''',0,False))
                 self.swords_talents.append(talent("Reaver",'''When you Attack during Challenges, you may also move one zone (p. 109) as
you charge towards your foe''',0,False))
                 self.swords_talents.append(talent("Two-handed Focus",'''If you are wielding a melee weapon with both hands during a Challenge, you
may Attack as a minor action with either a Pentacles or a Swords card.''',0,False))
                 self.swords_talents.append(talent("War Stories",'''As a Camp Action, tell your guild the story of some of your past adventures.
Maybe this was an adventure you've played out in-character, or maybe one in
your backstory. You—and everyone who listens and role-plays with you a little—
gets to choose one of the following benefits:
• They may charge an uncharged Bond.
• They gain an extra point of Resolve; this can bring their Resolve up to 5.''',0,False))
                 self.pentacles_talents = []
                 self.pentacles_talents.append(talent("Acrobat",'''You no longer need to test fate to climb sheer surfaces
or walk across narrow ledges or tightropes. You climb
and scamper along difficult or vertical terrain as easily as
walking. During Challenges, you may move this way as a
miscellaneous action, as easily as walking to a new zone.
Additionally, if you are prepared, you may treat a fall
as if it were 20’ shorter (p. 96). If you are not prepared
for a fall, you may spend a Resolve to treat it as if it were
20’ shorter.''',0,False))
                 self.pentacles_talents.append(talent("Ambusher",'''In the first round of a Challenge, whenever you would
deal damage, you deal 2 Wounds instead of 1.
Spend a Resolve to resist being ambushed. You raise a
hue and cry to warn your guild of the threat beforehand.''',0,False))
                 self.pentacles_talents.append(talent("Con Artist",'''If you spend a few minutes observing a person in
conversation or talking to them, you may bid lore to ask
the GM to reveal either one of their likes or their dislikes
(your choice); see page 99 for more on Disposition and
page 180 for more about likes and dislikes.''',0,False))
                 self.pentacles_talents.append(talent("Fight Dirty",'''During Challenges, you may Roughhouse as a
minor action with either a Pentacles or Swords card.
Additionally, you gain several new Roughhouse options:
• Exhaust
• Notch
• Silence''',0,False))
                 self.pentacles_talents.append(talent("Quick!",'''During Challenges, if you are wearing light or no armor,
you may treat Pentacles actions as interrupts''',0,False))
                 self.pentacles_talents.append(talent("Sneak",'''At any point, you may declare that you go sneaking.
This allows you to go dramatically off-stage.
Later, if you are not present in a scene and it’s at least
somewhat plausible that you could have snuck there,
spend a Resolve to arrive on the scene dramatically. If
a Challenge has yet to begin, this arrival counts as an
ambush (p. 110). If combat has already begun, nobody is
surprised because everybody is on edge—simply join the
flow of combat per usual.
If you go sneaking and all tension evaporates, you may
rejoin the scene by slinking out of the shadows. This
does not cost a Resolve.
This talent also gives you a new Camp Action: Infiltrate.
When you Infiltrate, you investigate a specific location
that you know of in your current dungeon level.
Thereafter, you may bid lore to ask the GM a specific
yes or no question about something you’d know having
infiltrated that location, e.g., “Is this door trapped?”, “Is
this room guarded?”, “Is the wizard’s bedroom on this
level?”, “Do the bandits have bows?”, “Were the orcs
green-skinned?”''',0,False))
                 self.pentacles_talents.append(talent("Up My Sleeve",'''You may declare that you have had a common, one-slot
item with you the whole time. Twice per Crawl (one for
each sleeve), spend a Resolve and declare that you had
a [blank] up your sleeve. This can include a lockpick, a
dagger, a handkerchief, an empty vial, a length of wire,
or anything else that the GM generally finds viable.''',0,False))
                 self.cups_talents = []
                 self.cups_talents.append(talent("Alchemy",'''This talent gives you a new Camp Action: Brew
Alchemy. When you Brew Alchemy, you use an alchemy
kit to turn any number of reagents you have into
alchemical substances. Reagents are harvested from the
bodies of Underworld monsters. Alchemical substances
are kept in hermetic bottles and divided into three
categories: potions, oils, and bombs. See Appendix B for
more information on alchemy.''',0,False))
                 self.cups_talents.append(talent("Beast Master",'''This talent allows you to train and issue commands to
your animal companions. As a Camp Action, you may
teach one animal companion one command. Normal
trained animals may learn up to three commands. It
is possible to retrain an animal with a new command,
replacing one of their previously mastered commands.
Pick from this list of commands (or new ones that the
GM approves):
• Sic ‘Em
• Get Help
• Heel
• Fetch
• Track
• Hunt
• Do a Trick
• Guard
• Stay
If you have mastered this talent, one animal you own
is considered your familiar. Familiars can learn five
different commands. Furthermore, if your familiar would
take a Wound that would kill them, you may spend a
Resolve to declare that they’re only at Death’s Door and
not actually dead.
More information about animal companions can be
found on page 34''',0,False))
                 self.cups_talents.append(talent("Bookworm",'''You have an almost encyclopedic knowledge of
everything you have read. Once you have used the Read
a Book Camp Action (p. 137), you may thereafter bid lore
to ask a question about the subject of that text. Keep
a list of books that you’ve read. These are treated like
motifs for the purpose of bidding lore, but don’t aid you
in tests of fate.''',0,False))    
                 self.cups_talents.append(talent("Chirurgeon",'''You may provide healing to your companions. You can
expend a poultice to Heal someone (p. 12). This effect
cannot be used to clear the Stressed condition.
Additionally, this talent gives you a new Camp Action:
Chirurgery. When you use Chirurgery on a non-Stressed
guild-mate using the Rest and Recover Camp Action,
you may Heal all of their Wounds.''',0,False))           
                 self.cups_talents.append(talent("Counsel",'''Any time during a Challenge, you may yell advice to
another adventurer and hand the player a card from your
hand. The card’s suit must match the action you counsel
them to take. The other player may play that card as long
as they use it to take your advice. In all other ways, it is
treated as a normal Challenge card (p. 112).
If you spend a Resolve when you use this talent,
the other player may play this card as an interrupt.
Otherwise, the standard one-card-per-turn rule remains
in effect (p. 113).
You may use this talent once per round.''',0,False))   
                 self.cups_talents.append(talent("High Chant",'''This talent gives you a new Camp Action: Perform the
High Chant. When you Perform the High Chant, speak
at least two stanzas of epic poetry for the table. If you
do so, you may select a number of cards from the minor
arcana discard pile equal to your Cups. These are called
inspiration cards. Distribute the cards to other players—
you may keep one for yourself. No player can ever have
more than one inspiration card. Inspiration cards may be
spent as actions during a Challenge. Alternatively, you
may spend your inspiration card instead of drawing from
the deck when you test fate or push fate. Inspiration
cards last until used or until the end of the session,
whichever comes first.''',0,False))   
                 self.cups_talents.append(talent("Loremaster",'''You are a student of ancient languages and lore. This
talent confers three advantages:
• You have knowledge of many languages and tongues.
You are assumed to be passingly fluent in any spoken
language that you might encounter.
• You can translate ancient scripts and runes. Translating
a short ancient runic passage that you encounter while
delving takes a watch or two. Translating a longer text
(such as a book) requires a City Action.
• When you bid lore, you may spend a Resolve instead
of spending a lore bid.''',0,False))   
                 self.wands_talents = []                              
                 self.wands_talents.append(talent("Counter-spell",'''You can counter the effects of sorcery with an effort of
will. There are two applications for this talent:
• You can stop enemy sorcerers from casting spells
in battle. During Challenges, if you can perceive a
sorcerer casting a spell, you may spend a Resolve to
Speak Incantations as an interrupt.
• If your Speak Incantations value is greater than the
enemy sorcerer’s total value, their spell fizzles out.
• If your Speak Incantations value is equal to or less
than the enemy’s total value, the spell fizzles out but
you must draw on the maleficence table (Appendix
A, p. 201) as the magic goes awry.
• You can negate a spell already in play. You may
spend a Resolve to immediately end the ongoing
effects of a spell.''',0,False))   
                 self.wands_talents.append(talent("Dwimmercraft",'''Suffused with the arcane arts, you can perform small (but
meaningful) expressions of magic. You may perform the
following minor effects:
• You may levitate an object in your zone that weighs
about 10 lbs. and that fits comfortably in one hand. You
have no fine motor control over this effect, but can
bring things to you, lift them up, or push them away.
• You may conjure a showy, harmless, and obviously
magical illusion—a shower of sparks, a colorful rainbow
stretched between your hands, a flickering image of
your first love.
• You conjure a simple illusion of something that you
can hold in one hand. Anybody that tries to interact
with this object will realize it’s an illusion, but the sight
of it is fairly convincing.
Additionally, by spending a Resolve, you can focus your
second sight for a watch. Second sight allows you to see
invisible and Shrouded things. You can perceive the true
form of any illusion. You can automatically tell when
things are magical or under enchantment. You can also
tell if somebody else is a sorcerer.
Using this talent during a Challenge counts as a
miscellaneous action.''',0,False)) 
                 self.wands_talents.append(talent("Gramarye",'''You have learned how to draw on the energies of the
far realms. Using this talent, you can release a blast
of magical energy up to one zone away through an
archwood wand, doing damage as a weapon. During
Challenges, Attacks with your wand count as Wands
actions (p. 119).
Additionally, you gain a new Camp Action: Make a Pact.
When you Make a Pact, choose to observe one or more
pacts from the facing page''',0,False)) 
                 self.wands_talents.append(talent("Magic of the Wastes",'''You may cast spells of the Wastes. The Wastes are a grim
place of death and decay. Spells of this realm deal with
matters of undeath, spread fear, or cause harm.''',0,False)) 
                 self.wands_talents.append(talent("Magic of the Weald",'''You may cast spells of the Weald. The Weald is a verdant
and wild place. Spells of this realm affect the elements,
command beasts, and reshape the natural world.''',0,False)) 
                 self.wands_talents.append(talent("Magic of the Weird",'''You may cast spells of the Weird. The Weird is a place
of dream, untouched by sanity. Spells of this realm
affect one’s mind and emotions, conjure illusions, and
bend reality.''',0,False)) 
                 self.wands_talents.append(talent("Magic of the Welkin",'''You may cast spells of the Welkin. The Welkin is a
bright and holy place. Spells of this realm deal with
angels, provide healing and protection, and invoke an
awful wonder.''',0,False)) 
                 self.human_arete_tasks = ["Getting married","Fulfilling an oath","Defeating a member of a rival house in fair tournament or duel"]
                 self.fay_arete_tasks = ["Killing something without using a weapon","Providing aid to a spirit","Making someone they’ve kissed cry"]
                 self.underfolk_arete_tasks = ["Crafting something that will last for centuries","Recovering a precious gem or work of fine art and hoarding it as a grave good","Discovering something secret and forgotten"]
                 self.orc_arete_tasks = ["Hoarding a skull from a class of monster your guild has never killed before","Hoarding a treasure of great worth","Slaying a monster at least twice your size"]



                 
class char_sheet(QMainWindow,Ui_HisMajestyTheWorm,character):


    def __init__(self):
        super().__init__()
        
        character.__init__(
            self,
            "",
            "",
            "",
            "",
            0,
            0,
            0,
            0,
            "",
            [],
            [],
            [],
            []
        )
        # Set up the UI generated by Qt Designer
        self.setupUi(self)
        
        self.inventory_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.inventory_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.path_talent_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.path_talent_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.belt_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.belt_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.lthand_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.lthand_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.rthand_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.rthand_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.motif_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.motif_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.guildmate_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.guildmate_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.taught_talent_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.taught_talent_table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.swords_box.valueChanged.connect(self.update_swords)
        self.pentacles_box.valueChanged.connect(self.update_pentacles)
        self.cups_box.valueChanged.connect(self.update_cups)
        self.wands_box.valueChanged.connect(self.update_wands)

        self.resolve_box.valueChanged.connect(self.update_resolve)
        self.lore_bids_box.valueChanged.connect(self.update_lore_bids)
        self.unspent_xp_box.valueChanged.connect(self.update_unspent_xp)

        self.inventory_table.cellClicked.connect(self.pack_item_clicked)
        self.belt_table.cellClicked.connect(self.belt_item_clicked)
        self.rthand_table.cellClicked.connect(self.rthand_item_clicked)
        self.lthand_table.cellClicked.connect(self.lthand_item_clicked)

        self.nameedit.textChanged.connect(self.update_name)
        self.languages_box.textChanged.connect(self.update_languages)
        self.quest_box.textChanged.connect(self.update_quest)
        self.conditions_box.textChanged.connect(self.update_conditions)

        self.kith_dropdown.currentTextChanged.connect(self.update_kith)
        self.kith_dropdown.currentTextChanged.connect(self.set_kin_choices)
        self.kin_dropdown.currentTextChanged.connect(self.update_kin)

        self.path_dropdown.currentTextChanged.connect(self.set_path_talents)
        self.path_talent_table.cellClicked.connect(self.show_talent_details)
        self.taught_talent_table.cellChanged.connect(self.update_taught_talents)

        self.motif_table.cellChanged.connect(self.update_motifs)
        self.guildmate_table.cellChanged.connect(self.update_bonds)

        self.actionSave_As.triggered.connect(self.save_as_clicked)
        self.actionOpen_Crawlspace_Inventory.triggered.connect(self.open_crawlspace_inventory)
        self.actionOpen.triggered.connect(self.open_clicked)
        self.actionOpen_Guildbook_Markdown.triggered.connect(self.open_guildbook_md)

        self.arete_check_1.stateChanged.connect(self.arete_1_state_change)
        self.arete_check_2.stateChanged.connect(self.arete_2_state_change)
        self.arete_check_3.stateChanged.connect(self.arete_3_state_change)

        self.helm_notch.stateChanged.connect(self.helm_notch_state_change)
        self.armor_notch_1.stateChanged.connect(self.armor_notch_1_state_change)
        self.armor_notch_2.stateChanged.connect(self.armor_notch_2_state_change)
        self.armor_notch_3.stateChanged.connect(self.armor_notch_3_state_change)

        self.lt_notch_1.stateChanged.connect(self.save_ltnotches)
        self.lt_notch_2.stateChanged.connect(self.save_ltnotches)
        self.lt_notch_3.stateChanged.connect(self.save_ltnotches)
        self.rt_notch_1.stateChanged.connect(self.save_rtnotches)
        self.rt_notch_2.stateChanged.connect(self.save_rtnotches)
        self.rt_notch_3.stateChanged.connect(self.save_rtnotches)
        self.lthand_table.inventoryChanged.connect(self.update_hand_notches)
        self.rthand_table.inventoryChanged.connect(self.update_hand_notches)
        self.belt_table.inventoryChanged.connect(self.update_hand_notches)
        self.inventory_table.inventoryChanged.connect(self.update_hand_notches)

        self.flicker1.stateChanged.connect(self.update_flickers)
        self.flicker2.stateChanged.connect(self.update_flickers)
        self.flicker3.stateChanged.connect(self.update_flickers)

        self.kin_wounded_box.stateChanged.connect(self.kin_wound_state_change)
        self.arete_wounded_box.stateChanged.connect(self.arete_wound_state_change)

        self.stressed_box.stateChanged.connect(self.stressed_state_change)
        self.hale_button.toggled.connect(lambda:self.update_health(0))
        self.staggered_button.toggled.connect(lambda:self.update_health(1))
        self.injured_button.toggled.connect(lambda:self.update_health(2))
        self.deaths_door_button.toggled.connect(lambda:self.update_health(3))

        
        self.set_kin_choices("Human")
        self.set_path_talents("Swords")
        self.update_kith("Human")
        self.taught_talents = [talent("",""),talent("","")]
        self.populate_taught_talents()
        self.populate_bonds()
        self.arete_task_1_complete = False
        self.arete_task_2_complete = False
        self.arete_task_3_complete = False
        self.helm_notched = False
        self.armor_notched_1 = False
        self.armor_notched_2 = False
        self.armor_notched_3 = False
        self.stressed = False
        self.motifs = ["","",""]
        self.bonds = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None] #dont have more than 20 bonds i dont wanna code error checking for this lmao :)
        self.health = "Hale"
        self.resolve = 0
        self.lore_bids = 0
        self.unspent_xp = 0
        self.helm_notched = False
        self.armor_notches = 0
        self.motifs = [None,None,None]
        self.languages = ""
        self.conditions = ""
        self.flickers = 0
        self.rthand = None
        self.lthand = None
        self.belt = None
        self.pack = None
        self.belt_list = [None,None,None,None]
        self.pack_list = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


        self.quest = ""


    def update_swords(self,value):
          self.swords = value
          return
    def update_pentacles(self,value):
        self.pentacles = value
        return
    def update_cups(self,value):
        self.cups = value
        return
    def update_wands(self,value):
        self.wands = value
        return
    def update_resolve(self,value):
        self.resolve = value
        return
    def update_lore_bids(self,value):
        self.lore_bids = value
        return
    def update_unspent_xp(self,value):
        self.unspent_xp = value
        return

    def update_name(self,text):
        self.name = text
    def update_languages(self):
        self.languages = self.languages_box.toPlainText()
    def update_conditions(self):
        self.conditions = self.conditions_box.toPlainText()
    def update_quest(self):
        self.quest = self.quest_box.toPlainText()


    def kin_wound_state_change(self, state):
        self.kithkin.kin_talent.wounded = self.kin_wounded_box.isChecked()

    def arete_wound_state_change(self, state):
        self.kithkin.arete_talent.wounded = self.arete_wounded_box.isChecked()


    def arete_1_state_change(self):
       if self.arete_check_1.isChecked():
            self.arete_task_1_complete = True
       else:
            self.arete_task_1_complete = False
    def arete_2_state_change(self):
       if self.arete_check_2.isChecked():
            self.arete_task_2_complete = True
       else:
            self.arete_task_2_complete = False
    def arete_3_state_change(self):
       if self.arete_check_3.isChecked():
            self.arete_task_3_complete = True
       else:
            self.arete_task_3_complete = False
    def helm_notch_state_change(self):
       if self.helm_notch.isChecked():
            self.helm_notched = True
       else:
            self.helm_notched = False
    def armor_notch_1_state_change(self):
       if self.armor_notch_1.isChecked():
            self.armor_notched_1 = True
       else:
            self.armor_notched_1 = False
       self.update_armor_notches()
        
    def armor_notch_2_state_change(self):
       if self.armor_notch_2.isChecked():
            self.armor_notched_2 = True
       else:
            self.armor_notched_2 = False
       self.update_armor_notches()
        
    def armor_notch_3_state_change(self):
       if self.armor_notch_3.isChecked():
            self.armor_notched_3 = True
       else:
            self.armor_notched_3 = False

       self.update_armor_notches()

    def update_armor_notches(self):
       self.armor_notches = (
            int(self.armor_notch_1.isChecked()) +
            int(self.armor_notch_2.isChecked()) +
            int(self.armor_notch_3.isChecked())
        )
    def stressed_state_change(self):
       if self.stressed_box.isChecked():
            self.stressed = True
       else:
            self.stressed = False

    def update_hand_notches(self):
        self.update_ltnotches()
        self.update_rtnotches()

    def update_ltnotches(self):
        if not self.lthand_table.inventory_items:
            return

        item = self.lthand_table.inventory_items[0]
        self.lthand = item
        if item is None:
            return


        
        notches = item.get("notches", 0)

        self.lt_notch_1.setChecked(notches >= 1)
        self.lt_notch_2.setChecked(notches >= 2)
        self.lt_notch_3.setChecked(notches >= 3)


    def save_ltnotches(self):
        if not self.lthand_table.inventory_items:
            return

        item = self.lthand_table.inventory_items[0]

        if item is None:
            return

        item["notches"] = (
            int(self.lt_notch_1.isChecked()) +
            int(self.lt_notch_2.isChecked()) +
            int(self.lt_notch_3.isChecked())
        )

        self.lthand = item
    def save_rtnotches(self):
        if not self.rthand_table.inventory_items:
            return

        item = self.rthand_table.inventory_items[0]

        if item is None:
            return

        item["notches"] = (
            int(self.rt_notch_1.isChecked()) +
            int(self.rt_notch_2.isChecked()) +
            int(self.rt_notch_3.isChecked())
        )

        self.rthand = item
    def update_rtnotches(self):
        if not self.rthand_table.inventory_items:
            return

        item = self.rthand_table.inventory_items[0]
        self.rthand = item
        if item is None:
            return


        notches = item.get("notches", 0)

        self.rt_notch_1.setChecked(notches >= 1)
        self.rt_notch_2.setChecked(notches >= 2)
        self.rt_notch_3.setChecked(notches >= 3)

    def update_flickers(self):
        self.flickers = (
            int(self.flicker1.isChecked()) +
            int(self.flicker2.isChecked()) +
            int(self.flicker3.isChecked())
        )
    def display_flickers(self):


        flickers = self.flickers
        self.flicker1.setChecked(flickers >= 1)
        self.flicker2.setChecked(flickers >= 2)
        self.flicker3.setChecked(flickers >= 3)






    def update_health(self,num):
        self.health = self.status[num]


    def update_kith(self,kith):
         self.kith = kith
         self.populate_arete_tasks()

    def update_motifs(self, row, column):
        item = self.motif_table.item(row, column)

        if item is not None:
            self.motifs[row] = item.text()

            self.populate_motifs()

    def update_taught_talents(self, row, column):
        if row == 0:
            return

        item = self.taught_talent_table.item(row, column)

        if item is None:
            return

        talent_index = row - 1

        if talent_index >= len(self.taught_talents):
            return

        self.taught_talents[talent_index].name = item.text()
    def update_bonds(self, row, column):
        if row == 0: return
        newrow = row - 1
        checkbox = self.guildmate_table.cellWidget(row, 2)
        guildmate_item = self.guildmate_table.item(row, 0)
        bond_item = self.guildmate_table.item(row, 1)
        if guildmate_item is None or bond_item is None:
            return
        
        charged = False
        if checkbox is not None:
            charged = checkbox.isChecked()
        self.bonds[newrow] = bond(self.guildmate_table.item(row,0).text(),self.guildmate_table.item(row,1).text(),charged)

        self.populate_bonds()
    
    def populate_arete_tasks(self):
         match (self.kith):
            case "Human":
              self.arete_tasks = self.human_arete_tasks
            case "Fay":
              self.arete_tasks = self.fay_arete_tasks
            case "Underfolk":
              self.arete_tasks = self.underfolk_arete_tasks
            case "Orc":
              self.arete_tasks = self.orc_arete_tasks
            case _:
              self.arete_tasks = self.human_arete_tasks
         self.arete_task_1.setText(self.arete_tasks[0])
         self.arete_task_2.setText(self.arete_tasks[1])
         self.arete_task_3.setText(self.arete_tasks[2])

    def set_kin_choices(self,kith):
         self.kin_dropdown.clear()
         match (kith):
             case "Human":
                  self.kithkin = self.human
                  choices = ["Great House"]
             case "Fay":
                   choices = ["High Elf", "Dark Elf", "Wood Elf", "Gnome"]
             case "Underfolk":
                choices = ["Dwarf","Halfling","Troll"]
             case "Orc":
                   choices = ["Earthblood","Seablood","Stormblood","Fireblood"]
             case _:
                   choices = []
         self.kin_dropdown.addItems(choices)
         return

    def update_kin(self, kin):
        match kin:
            case "Great House":
                self.kin = "Great House"
                self.kithkin = self.human

            case "High Elf":
                self.kin = "High Elf"
                self.kithkin = self.high_elf

            case "Dark Elf":
                self.kin = "Dark Elf"
                self.kithkin = self.dark_elf

            case "Wood Elf":
                self.kin = "Wood Elf"
                self.kithkin = self.wood_elf

            case "Gnome":
                self.kin = "Gnome"
                self.kithkin = self.gnome

            case "Dwarf":
                self.kin = "Dwarf"
                self.kithkin = self.dwarf

            case "Halfling":
                self.kin = "Halfling"
                self.kithkin = self.halfling

            case "Troll":
                self.kin = "Troll"
                self.kithkin = self.troll

            case "Earthblood":
                self.kin = "Earthblood"
                self.kithkin = self.earthblood

            case "Seablood":
                self.kin = "Seablood"
                self.kithkin = self.seablood

            case "Stormblood":
                self.kin = "Stormblood"
                self.kithkin = self.stormblood

            case "Fireblood":
                self.kin = "Fireblood"
                self.kithkin = self.fireblood
        self.set_kin_and_arete_talents()
        return


    def set_kin_and_arete_talents(self):
         self.kin_talent_name.setText(self.kithkin.kin_talent.name)
         self.arete_talent_name.setText(self.kithkin.arete_talent.name)
         self.kin_talent_desc.setText(self.kithkin.kin_talent.desc)
         self.arete_talent_desc.setText(self.kithkin.arete_talent.desc)
         return

    def set_path_talents(self,path):
         self.swords_box.setMaximum(3)
         self.pentacles_box.setMaximum(3)
         self.cups_box.setMaximum(3)
         self.wands_box.setMaximum(3)
         self.path = path
         match (self.path):
              case "Swords":
                   self.path_talents = self.swords_talents
                   self.swords_box.setMaximum(4)
                   self.swords_box.setValue(4)
              case "Pentacles":
                   self.path_talents = self.pentacles_talents
                   self.pentacles_box.setMaximum(4)
                   self.pentacles_box.setValue(4)
              case "Cups":
                   self.path_talents = self.cups_talents
                   self.cups_box.setMaximum(4)
                   self.cups_box.setValue(4)
              case "Wands":
                   self.path_talents = self.wands_talents
                   self.wands_box.setMaximum(4)
                   self.wands_box.setValue(4)
              case _:
                   self.path_talents = self.swords_talents
                   self.swords_box.setMaximum(4)
                   self.swords_box.setValue(4)
         self.populate_path_talents()
    def populate_bonds(self):
        if not self.bonds: return
        self.guildmate_table.blockSignals(True)
        self.guildmate_table.setItem(0, 0, QTableWidgetItem("Guildmate"))
        self.guildmate_table.setItem(0, 1, QTableWidgetItem("Bond"))
        self.guildmate_table.setItem(0, 2, QTableWidgetItem("Charged?"))
        for row, item in enumerate(self.bonds):
            if item is None: continue
            table_item = QTableWidgetItem(item.guildmate)
            self.guildmate_table.setItem(row+1, 0, table_item)
            table_item2 = QTableWidgetItem(item.bond)
            self.guildmate_table.setItem(row+1, 1, table_item2)



            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(item.charged)
            checkbox.setStyleSheet("margin-left: 10px;")
            checkbox.stateChanged.connect(lambda state, r = row:self.update_charged_bond(r,state))
            self.guildmate_table.setCellWidget(row+1, 2, checkbox) 
        
        self.guildmate_table.blockSignals(False)
    def update_charged_bond(self, row,state):  
        if  self.bonds[row] is None: return 
        if state:
            self.bonds[row].charged = True
        else:
            self.bonds[row].charged = False



    def populate_motifs(self):

        self.motif_table.blockSignals(True)
        self.motif_table.setItem(0, 0, QTableWidgetItem("Motif"))
        self.motif_table.setItem(1, 0, QTableWidgetItem("Motif"))
        self.motif_table.setItem(2, 0, QTableWidgetItem("Motif"))
        for row, item in enumerate(self.motifs):
            table_item = QTableWidgetItem(item)
            self.motif_table.setItem(row, 1, table_item)
        self.motif_table.blockSignals(False)
        self.motif_table.resizeRowsToContents()
        self.motif_table.resizeColumnsToContents()


    def populate_path_talents(self):
        self.path_talent_table.blockSignals(True)
        self.path_talent_table.setColumnCount(3)
        self.path_talent_table.setRowCount(8)
        self.path_talent_table.setHorizontalHeaderLabels(["Talent"])
        self.path_talent_table.setItem(0, 0, QTableWidgetItem("Path Talent"))
        self.path_talent_table.setItem(0, 1, QTableWidgetItem("XP"))
        self.path_talent_table.setItem(0, 2, QTableWidgetItem("Wounded?"))
        for row, item in enumerate(self.path_talents):

            table_item = QTableWidgetItem(item.name)
            self.path_talent_table.setItem(row+1, 0, table_item)
            # Spin box
            spin = MasterySpinBox()
            spin.setRange(0, 7)
            spin.setValue(item.xp)
            spin.valueChanged.connect(lambda value, r = row:self.update_path_talent_properties(r,value,"xp"))
            self.path_talent_table.setCellWidget(row+1, 1, spin)

            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(item.wounded)
            checkbox.setStyleSheet("margin-left: 10px;")
            checkbox.stateChanged.connect(lambda state, r = row:self.update_path_talent_properties(r,state,"wounded"))
            self.path_talent_table.setCellWidget(row+1, 2, checkbox) 
        self.path_talent_table.blockSignals(False)
            

        
    def update_path_talent_properties(self, row,state,property):  
        if  self.path_talents[row] is None: return 
        match property:
            case "xp":
                self.path_talents[row].xp = state
            case "wounded":
                
                self.path_talents[row].wounded = state
            case _:
                return
    
    def populate_taught_talents(self):
        self.taught_talent_table.blockSignals(True)
        self.taught_talent_table.setColumnCount(3)
        self.taught_talent_table.setRowCount(3)
        self.taught_talent_table.setHorizontalHeaderLabels(["Talent"])
        self.taught_talent_table.setItem(0, 0, QTableWidgetItem("Taught Talent"))
        self.taught_talent_table.setItem(0, 1, QTableWidgetItem("XP"))
        self.taught_talent_table.setItem(0, 2, QTableWidgetItem("Wounded?"))
        for row, item in enumerate(self.taught_talents):
            table_item = QTableWidgetItem(item.name)
            self.taught_talent_table.setItem(row+1, 0, table_item)
            # Spin box
            spin = MasterySpinBox()
            spin.setRange(0, 7)
            spin.setValue(item.xp)
            spin.valueChanged.connect(lambda value, r = row:self.update_taught_talent_properties(r,value,"xp"))
            self.taught_talent_table.setCellWidget(row+1, 1, spin)

            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(item.wounded)
            checkbox.setStyleSheet("margin-left: 10px;")
            checkbox.stateChanged.connect(lambda state, r = row:self.update_taught_talent_properties(r,state,"wounded"))
            self.taught_talent_table.setCellWidget(row+1, 2, checkbox) 

        
        self.taught_talent_table.resizeRowsToContents()
        self.taught_talent_table.resizeColumnsToContents()
        self.taught_talent_table.blockSignals(False)
    def update_taught_talent_properties(self, row,state,property):  
        if  self.taught_talents[row] is None: return 
        match property:
            case "xp":
                self.taught_talents[row].xp = state
            case "wounded":
                
                self.taught_talents[row].wounded = state
            case _:
                return   
    def populate_pack(self, pack):
        if not self.pack: return
        self.inventory_table.setRowCount(10)
        self.inventory_table.setColumnCount(2)

        self.inventory_table.inventory_name = "pack"
        self.inventory_table.inventory_items = pack

        self.pack_list = pack

        self.inventory_table.clearContents()

        for row, item in enumerate(pack):

            if item is None:
                continue

            table_item = QTableWidgetItem(item["name"])

            if row < 10:
                self.inventory_table.setItem(row, 0, table_item)
            else:
                self.inventory_table.setItem(row - 10, 1, table_item)

        self.inventory_table.resizeColumnsToContents()
        self.inventory_table.resizeRowsToContents()
    def populate_belt(self, belt):
        if not self.belt: return
        self.belt_table.setRowCount(2)
        self.belt_table.setColumnCount(2)

        self.belt_table.inventory_name = "belt"
        self.belt_table.inventory_items = belt

        self.belt_list = belt

        self.belt_table.clearContents()

        for row, item in enumerate(belt):

            if item is None:
                continue

            table_item = QTableWidgetItem(item["name"])

            if row < 2:
                self.belt_table.setItem(row, 0, table_item)
            else:
                self.belt_table.setItem(row - 2, 1, table_item)

        self.belt_table.resizeColumnsToContents()
        self.belt_table.resizeRowsToContents()

    def populate_hands(self, rthand, lthand):

        self.rthand = rthand
        self.lthand = lthand

        self.rthand_table.setRowCount(1)
        self.rthand_table.setColumnCount(1)

        self.rthand_table.inventory_name = "rthand"
        self.rthand_table.inventory_items = [rthand]

        self.rthand_table.clearContents()

        if rthand is not None:
            self.rthand_table.setItem(
                0,
                0,
                QTableWidgetItem(rthand["name"])
            )

        self.lthand_table.setRowCount(1)
        self.lthand_table.setColumnCount(1)

        self.lthand_table.inventory_name = "lthand"
        self.lthand_table.inventory_items = [lthand]

        self.lthand_table.clearContents()

        if lthand is not None:
            self.lthand_table.setItem(
                0,
                0,
                QTableWidgetItem(lthand["name"])
            )



    def pack_item_clicked(self, row, column):
        item_index = row + (column * 10)
        item = self.pack_list[item_index]

        self.show_item_details(
            item,
            self.pack_list,
            item_index,
            "pack"
        )
    def belt_item_clicked(self, row, column):
        item_index = row + (column * 2)
        item = self.belt_list[item_index]

        self.show_item_details(
            item,
            self.belt_list,
            item_index,
            "belt"
        )

    def rthand_item_clicked(self):
        item = self.rthand

        self.show_item_details(
            item,
            [item],
            0,
            "rthand"
        )

    def lthand_item_clicked(self):
        item = self.lthand
        self.show_item_details(
            item,
            [item],
            0,
            "lthand"
        )


    def show_item_details(self,item,inventory_list,item_index,loc):
        self.edit_item(item,inventory_list,item_index,loc) #TODO: clean up call later
        self.populate_hands(self.rthand,self.lthand)
        self.populate_belt(self.belt)
        self.populate_pack(self.pack)
    
    def edit_item(self, item, inventory_list=None, item_index=None,loc = None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Item")
        dialog.resize(400, 300)

        layout = QVBoxLayout(dialog)

        # Item name
        name_label = QLabel("Name:")
        name_box = QLineEdit()

        if item is not None:
            name_box.setText(item.get("name", ""))

        # Description
        description_label = QLabel("Description:")
        description_box = QTextEdit()

        if item is not None:
            description_box.setPlainText(
                item.get("desc", "No description available.")
            )
        else:
            description_box.setPlainText("")

        save_button = QPushButton("Save")

        layout.addWidget(name_label)
        layout.addWidget(name_box)
        layout.addWidget(description_label)
        layout.addWidget(description_box)
        layout.addWidget(save_button)

        def save_item():
            new_name = name_box.text().strip()

            # Don't allow an empty item name
            if not new_name:
                QMessageBox.warning(
                    dialog,
                    "Invalid Name",
                    "The item name cannot be empty."
                )
                return

            if item is not None:
                # Edit existing item
                item["name"] = new_name
                item["desc"] = description_box.toPlainText()

            else:
                # Create new item
                new_item = {
                    "name": new_name,
                    "desc": description_box.toPlainText(),
                    "notches": 0
                }

                if inventory_list is not None and item_index is not None:
                    inventory_list[item_index] = new_item
            match loc:
                case "rthand":
                    if item is not None:
                        self.rthand = item
                    else:
                        self.rthand = new_item
                case "lthand":
                    if item is not None:
                        self.lthand = item
                    else:
                        self.lthand = new_item 
                case "belt":
                    self.belt = inventory_list
                case "pack":
                    self.pack = inventory_list
            dialog.accept()

        save_button.clicked.connect(save_item)

        dialog.exec_()




    def show_talent_details(self,row,column):
             talent = self.path_talents[row-1]
             QMessageBox.information(
        self,
        talent.name,
        talent.desc
    )
    def create_save_file(self,filename):
         

           sheet = {
           "state" : {
                         "swords":self.swords,
                         "pentacles":self.pentacles,
                         "cups":self.cups,
                         "wands":self.wands,
                         "name":self.name,
                         "path":self.path,
                         "kith":self.kith,
                         "kin":self.kin,
                         "health":self.health,
                         "stressed":self.stressed,
                         "resolve":self.resolve,
                         "lore bids":self.lore_bids,
                         "quest":self.quest,
                         "languages":self.languages,
                         "conditions":self.conditions,
                         "arete tasks":self.arete_tasks,
                         "motifs":self.motifs,
                         "bonds": [x.to_dict() if x is not None else None for x in self.bonds],
                         "helm notch":self.helm_notched,
                         "armor notches":self.armor_notches,
                         "flickers":self.flickers,
                         "unspent xp":self.unspent_xp


           },
           "talents" : {
                         "kin talent":self.kithkin.kin_talent.name,
                         "kin wounded":self.kithkin.kin_talent.wounded,
                         "arete talent":self.kithkin.arete_talent.name,
                         "arete wounded":self.kithkin.arete_talent.wounded,
                         "path talents":[x.to_dict() for x in self.path_talents if x is not None],
                         "taught talents":[x.to_dict() for x in self.taught_talents if x is not None]
           },
           "inventory" : {
                         "name":self.name, #for backwards compatibility with crawlspace
                         "rtHand":self.rthand,
                         "ltHand":self.lthand,
                         "belt":self.belt,
                         "pack":self.pack
                         
           }
             }
           
           if not os.path.exists(APP_DIR / "Save_Files"): os.makedirs(APP_DIR / "Save_Files")
           save_path = APP_DIR / "Save_Files" / f"{filename}"
           with open(save_path, "w", encoding="utf-8") as file:
                json.dump(sheet, file, indent=4)


    

    def save_as_clicked(self):
        save_folder = APP_DIR / "Save_Files"
        if save_folder.exists():
         start_location = str(save_folder)
        else:
         start_location = str(APP_DIR)

        filename, _ = QFileDialog.getSaveFileName(
        self,
        "Save As",
        start_location,
        "JSON Files (*.json);;All Files (*.*)"
        )
        if filename:
          self.create_save_file(filename)

    def open_clicked(self):
        save_folder = APP_DIR / "Save_Files"
        if save_folder.exists():
            start_location = str(save_folder)
        else:
            start_location = str(APP_DIR)
        filename, _ = QFileDialog.getOpenFileName(
        self,
        "Open File",
        start_location,
        "All Files (*.*)"
        )

        if filename:
           self.load_saved_character(filename)
    def open_crawlspace_inventory(self):
        save_folder = APP_DIR / "Save_Files"
        if save_folder.exists():
            start_location = str(save_folder)
        else:
            start_location = str(APP_DIR)
        filename, _ = QFileDialog.getOpenFileName(
        self,
        "Open File",
        start_location,
        "All Files (*.*)"
        )

        if filename:
           self.load_inventory_save(filename)

    def open_guildbook_md(self):
        save_folder = APP_DIR / "Save_Files"
        if save_folder.exists():
            start_location = str(save_folder)
        else:
            start_location = str(APP_DIR)
        filename, _ = QFileDialog.getOpenFileName(
        self,
        "Open File",
        start_location,
        "All Files (*.*)"
        )

        if filename:
           self.load_guildbook_md(filename)
    
    def load_inventory_save(self,filename):
         file = Path(filename)
         if not file.exists():
              return
         with open(file,"r",encoding="utf-8") as f:
              inventory = json.load(f)
         self.rthand = inventory["inventory"]["rtHand"]
         self.lthand = inventory["inventory"]["ltHand"]
         self.belt = inventory["inventory"]["belt"]
         self.pack = inventory["inventory"]["pack"]
         self.populate_pack(self.pack)
         self.populate_belt(self.belt)
         self.populate_hands(self.rthand,self.lthand)

    def load_saved_character(self,filename):
         file = Path(filename)
         if not file.exists():
              print("File does not exist")
         with open(file,"r",encoding="utf-8") as f:
              sheet = json.load(f)
        #load state variables
         self.swords = sheet["state"]["swords"]

         self.pentacles = sheet["state"]["pentacles"]
         self.cups = sheet["state"]["cups"]
         self.wands = sheet["state"]["wands"]
         self.name = sheet["state"]["name"]
         self.path = sheet["state"]["path"]
         self.kith = sheet["state"]["kith"]    
         self.kin = sheet["state"]["kin"]    
         self.health = sheet["state"]["health"]
         self.stressed = sheet["state"]["stressed"]
         self.resolve = sheet["state"]["resolve"]
         self.lore_bids = sheet["state"]["lore bids"]
         self.name = sheet["state"]["name"]
         self.path = sheet["state"]["path"]
         self.kith = sheet["state"]["kith"]    
         self.kin = sheet["state"]["kin"]      
         self.quest = sheet["state"]["quest"] 
         self.languages = sheet["state"]["languages"] 
         self.conditions = sheet["state"]["conditions"] 
         self.arete_tasks = sheet["state"]["arete tasks"] 
         self.motifs = sheet["state"]["motifs"] 
         self.helm_notched = sheet["state"]["helm notch"] 
         self.armor_notches = sheet["state"]["armor notches"] 
         self.flickers = sheet["state"]["flickers"]
         self.unspent_xp = sheet["state"]["unspent xp"]
         self.bonds = []
         for x in sheet["state"]["bonds"]:
             if x == None:
                 b = x
             else:
                 b = bond(x["guildmate"],x["bond"],x["charged"])
             self.bonds.append(b)            



        #load inventory
         self.rthand = sheet["inventory"]["rtHand"]
         self.lthand = sheet["inventory"]["ltHand"]
         self.belt = sheet["inventory"]["belt"]
         self.pack = sheet["inventory"]["pack"]

        #display state
         self.nameedit.setText(self.name)
         self.swords_box.setValue(self.swords)
         self.pentacles_box.setValue(self.pentacles)
         self.cups_box.setValue(self.cups)
         self.wands_box.setValue(self.wands)
         path_index = self.path_dropdown.findText(self.path)

         self.path_talent_table.blockSignals(True)
         if path_index != -1:
             self.path_dropdown.setCurrentIndex(path_index)

         self.set_path_talents(self.path)
         kith_index = self.kith_dropdown.findText(self.kith)

         if kith_index != -1:
             self.kith_dropdown.setCurrentIndex(kith_index)

         self.set_kin_choices(self.kith)

         kin_index = self.kin_dropdown.findText(self.kin)
         if kin_index != -1:
          self.kin_dropdown.setCurrentIndex(kin_index)
         self.update_kin(self.kin)
         self.resolve_box.setValue(self.resolve)
         self.lore_bids_box.setValue(self.lore_bids)
         self.unspent_xp_box.setValue(self.unspent_xp)
         self.languages_box.setText(self.languages)
         self.conditions_box.setText(self.conditions)

         self.quest_box.setText(self.quest)
         self.populate_motifs()
         self.populate_bonds()

         self.helm_notch.setChecked(self.helm_notched)
         self.armor_notch_1.setChecked(self.armor_notches >= 1)
         self.armor_notch_2.setChecked(self.armor_notches >= 2)
         self.armor_notch_3.setChecked(self.armor_notches >= 3)
                 #load talents. reconstruct kin, and arete so no need to load saved results. keep them in json for ease of parsing and possible custom talents later
         self.kithkin.kin_talent.wounded = sheet["talents"]["kin wounded"]
         self.kithkin.arete_talent.wounded = sheet["talents"]["arete wounded"]


         self.stressed_box.setChecked(self.stressed)
         match (self.health):
             case 0:
                 self.hale_button.setChecked(True)
             case 1:
                 self.staggered_button.setChecked(True)
             case 2:
                 self.injured_button.setChecked(True)
             case 3:
                 self.deaths_door_button.setChecked(True)
             case _:
                 self.hale_button.setChecked(True)


         
    
        #display inventory
         self.populate_pack(self.pack)
         self.populate_belt(self.belt)
         self.populate_hands(self.rthand,self.lthand)
         self.update_hand_notches()
         self.display_flickers()

        #display and load talents

         self.path_talents = []
         self.taught_talents = []
         for x in sheet["talents"]["path talents"]:
             if x == None:
                 t = x
             else:
                 t = talent(x["name"],x["desc"],x["xp"],x["wounded"])
             self.path_talents.append(t)
         for x in sheet["talents"]["taught talents"]:
             if x == None:
                 t = x
             else:
                 t = talent(x["name"],x["desc"],x["xp"],x["wounded"])
             self.taught_talents.append(t)
         self.populate_path_talents()
         self.populate_taught_talents()

         self.kin_wounded_box.blockSignals(True)
         self.arete_wounded_box.blockSignals(True)
         self.kin_wounded_box.setChecked(sheet["talents"]["kin wounded"])
         self.arete_wounded_box.setChecked(sheet["talents"]["arete wounded"])
         self.kin_wounded_box.blockSignals(False)
         self.arete_wounded_box.blockSignals(False)
         self.path_talent_table.blockSignals(False)

    def load_guildbook_md(self,filename):
        file = Path(filename)
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        parts = text.split("---", 2)

        if len(parts) < 3:
            raise ValueError("Character file does not contain YAML front matter.")

        attributes = yaml.safe_load(parts[1])
        markdown = parts[2]


        self.name = attributes["name"]
        self.kith = attributes["kith"]
        self.kin = attributes["kin"]
        self.swords = attributes["swords"]
        self.pentacles = attributes["pentacles"]
        self.cups = attributes["cups"]
        self.wands = attributes["wands"]                        
        self.motifs = attributes["motifs"]
        

        self.populate_motifs()
        path = attributes["path"]

        path_map = {
            "Path of Swords": "Swords",
            "Path of Pentacles": "Pentacles",
            "Path of Cups": "Cups",
            "Path of Wands": "Wands"
        }

        self.path = path_map.get(path, path)
        current, maximum = map(int, attributes["resolve"].split("/"))
        self.resolve = current

        #display state
        self.nameedit.setText(self.name)
        self.swords_box.setValue(self.swords)
        self.pentacles_box.setValue(self.pentacles)
        self.cups_box.setValue(self.cups)
        self.wands_box.setValue(self.wands)
        path_index = self.path_dropdown.findText(self.path)

        self.path_talent_table.blockSignals(True)
        if path_index != -1:
            self.path_dropdown.setCurrentIndex(path_index)

        self.set_path_talents(self.path)
        kith_index = self.kith_dropdown.findText(self.kith)

        if kith_index != -1:
            self.kith_dropdown.setCurrentIndex(kith_index)

        self.set_kin_choices(self.kith)

        kin_index = self.kin_dropdown.findText(self.kin)
        if kin_index != -1:
            self.kin_dropdown.setCurrentIndex(kin_index)
        self.update_kin(self.kin)
        self.resolve_box.setValue(self.resolve)



if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = char_sheet()
    window.show()
    sys.exit(app.exec_())
