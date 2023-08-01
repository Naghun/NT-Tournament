# NT Tournament - Realms Chosen

## About

Realms Chosen is a browser game developed by a solo developer. The game's logic and backend are built using Python with the Django Framework, while the frontend is designed using vanilla HTML, CSS, and JavaScript.

## Game Description
Realms Chosen is an evolving card game featuring 80 unique cards divided into 4 races, each with 20 heroes.

The current races in the game are Humans, Aliens, Creatures, and Fantasy. Each card, or hero, possesses specific attributes that play a vital role either in battles or in defining their initial strength. The game introduces a tier system, where the tier of a hero determines their strength within their race. For instance, a tier 1 Human may not be as strong as a tier 1 Alien.

The attributes include Health, Speed, Attack, Defense, Crit, and Fatigue. During battles, only Fatigue values change, starting at 0, others are set before battle begins. The tournament progresses with 8 chosen warriors from each class heading to the bonus room, where they draw bonuses. These bonuses can be tier 1, 2, or 3, either adding positive stats to attributes or subtracting them. In the bonus room, heroes have the chance to draw positive bonuses that enhance their Crit chance. This unique opportunity is the only way for heroes to gain Crit bonuses, making the bonus room a pivotal moment before battles, where heroes can significantly influence the outcome of their fights. Currently, bonuses are determined through random number generation (RNG).

After the bonuses are chosen, pairs are drawn, and the battle begins. Class bonuses come into play as well, where one class may have an advantage over another, forming a circular advantage system: Humans > Creatures > Fantasy > Aliens > Humans... The hero with the higher Speed launches the first attack, and the attack's strength is calculated based on their Attack after the opponent's Defense percentage is deducted. The resulting value reduces the opponent's Health accordingly. When a hero's Health reaches 0, the other one advances with their remaining Health.

Heroes with a Crit bonus have a chance to perform critical strikes during attacks, dealing 1.5 times their normal Attack value. At the end of each battle, the hero's Fatigue is accounted for based on the number of rounds fought. Fatigue affects their Speed and Attack, and these values persist until the end of the tournament. Fatigue can decrease stats again depending on the duration of their subsequent battles.

After determining the winner, all cards return to their initial values, the number of tournament changes, and the victorious hero gains one victory. Additionally, based on the tier, heroes receive attribute increases. For example, a tier 1 hero gains attribute increases every 5 victories, while a tier 4 hero recieves attribute boost with just 1 victory, attribute changes will be saved automatically and heroes will start next tournament with increased values set as default values.

The game starts in a yet undeveloped world, and the first tournament begins in day 1, year 1. Subsequent tournaments increase days and years automatically, featuring 32 warriors in an elimination-style competition, with only one emerging as the ultimate champion.

Furthermore, it is important to note that the game currently does not provide players with the ability to choose their champions or classes. At this stage, Realms Chosen remains a prototype, with the game unfolding automatically as the interactions between heroes take precedence. However, there are exciting plans for future extensions, and the game aims to evolve into an interactive experience where players can actively participate in selecting their champions and classes. As development progresses, the game's mechanics will be refined, introducing player agency and creating a deeper, engaging experience. Stay tuned for updates as we continue to shape the future of Realms Chosen!

Embark on an epic journey and lead your chosen warriors to victory in Realms Chosen! Face strategic challenges and dynamic battles as you unravel the mysteries of this fascinating card game. Will you be the last hero standing and claim victory in the ever-evolving Realms Chosen world? The stage is set; your adventure awaits!

## Game Review
** Realms Chosen ** is a browser game that aims to bring to life countless notebooks of my youth, where I manually recorded every step and spent days of my childhood. While there may be similar games out there, this game is the product of my imagination, born during my childhood when different cards like Yu-Gi-Oh! and Pokémon were a common staple in the backpacks of every student.
Throughout my life, I've always wanted to create a world of my own warriors representing different classes or races, who would bring glory to their respective factions while also progressing and growing stronger. I yearned for something where victory wasn't guaranteed for the strongest, and where the weaker could emerge triumphant, albeit with a stroke of luck. Achieving such complexity in my childhood was quite challenging, as all calculations were manually written in notebooks, and it remained nothing more than a dream.

Recently, I had the opportunity to fulfill the dreams of my younger self, and I promise him that this is only the beginning. Just as he was passionate about his game and desires, I will be equally zealous in making this into something greater, with never-ending updates and expansions. I hope that those of you who read this review and venture into my game will see the potential for something much grander and inclusive for all ages, rather than just a dream of a young boy.

The game, Realms Chosen, is a testament to my childhood aspirations, and I am excited to embark on this journey of turning it into something beyond my wildest imagination. I want to share this enthusiasm with you, the players, as we create a truly unforgettable gaming experience together. Thank you for joining me on this adventure, and I hope you find as much joy in playing as I found in creating it. Let's make dreams a reality!

## Requirements
Before running the project, please make sure you have the necessary dependencies installed. The required packages and their versions are listed in the `requirements.txt` file.

To install the dependencies, run the following command:
...Command  Shell
pip install -r requirements.txt

## TODO list
Todos for this applications are listed in the `ToDo.md` file.

## Created by
Abdullah Sinanović

**Copyright Notice:**
This game uses images whose rights I do not own, and I do not intend to publish it anywhere. It serves the purpose of improving my skills as a programmer until I acquire the necessary rights or create my own heroes and all other assets for which I have the proper rights to use.

:sparkles: **Welcome to the Realms Chosen** :sparkles:
