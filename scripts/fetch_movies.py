import os
import csv
import random
from collections import defaultdict

# Define genre distribution we want to achieve
TARGET_GENRES = {
    "Drama": 40,
    "Comedy": 30,
    "Action": 25,
    "Thriller": 25,
    "Adventure": 20,
    "Horror": 20,
    "Romance": 20,
    "Sci-Fi": 20,
    "Fantasy": 15,
    "Crime": 15,
    "Animation": 15,
    "Mystery": 15,
    "Biography": 10,
    "Family": 10,
    "War": 8,
    "Music": 8,
    "Documentary": 5,
    "Western": 5,
    "Musical": 5,
    "Sport": 5,
    "History": 5,
}

# Sample movie data - these are real movies with actual plots
MOVIES = [
    {
        "title": "Jurassic Park",
        "year": 1993,
        "genre": "Adventure, Sci-Fi",
        "plot": "A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose."
    },
    {
        "title": "The Social Network",
        "year": 2010,
        "genre": "Biography, Drama",
        "plot": "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea, and by the co-founder who was later squeezed out of the business."
    },
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Action, Adventure, Sci-Fi",
        "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama",
        "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "genre": "Crime, Drama",
        "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    },
    # Additional movies
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "genre": "Crime, Drama",
        "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action, Crime, Drama",
        "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "title": "Schindler's List",
        "year": 1993,
        "genre": "Biography, Drama, History",
        "plot": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."
    },
    {
        "title": "The Lord of the Rings: The Return of the King",
        "year": 2003,
        "genre": "Adventure, Fantasy, Drama",
        "plot": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring."
    },
    {
        "title": "Fight Club",
        "year": 1999,
        "genre": "Drama",
        "plot": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more."
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "genre": "Action, Sci-Fi",
        "plot": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "genre": "Drama, Romance",
        "plot": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75."
    },
    {
        "title": "Goodfellas",
        "year": 1990,
        "genre": "Crime, Drama, Biography",
        "plot": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito in the Italian-American crime syndicate."
    },
    {
        "title": "The Silence of the Lambs",
        "year": 1991,
        "genre": "Crime, Drama, Thriller",
        "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": "Adventure, Drama, Sci-Fi",
        "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "title": "The Prestige",
        "year": 2006,
        "genre": "Drama, Mystery, Sci-Fi",
        "plot": "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other."
    },
    {
        "title": "The Departed",
        "year": 2006,
        "genre": "Crime, Drama, Thriller",
        "plot": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston."
    },
    {
        "title": "Titanic",
        "year": 1997,
        "genre": "Drama, Romance",
        "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
    },
    {
        "title": "Parasite",
        "year": 2019,
        "genre": "Drama, Thriller, Comedy",
        "plot": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."
    },
    {
        "title": "The Lion King",
        "year": 1994,
        "genre": "Animation, Adventure, Drama",
        "plot": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."
    },
    {
        "title": "Spirited Away",
        "year": 2001,
        "genre": "Animation, Adventure, Fantasy",
        "plot": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts."
    },
    {
        "title": "The Shape of Water",
        "year": 2017,
        "genre": "Drama, Fantasy, Romance",
        "plot": "At a top secret research facility in the 1960s, a lonely janitor forms a unique relationship with an amphibious creature that is being held in captivity."
    },
    {
        "title": "Get Out",
        "year": 2017,
        "genre": "Horror, Mystery, Thriller",
        "plot": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point."
    },
    {
        "title": "CODA",
        "year": 2021,
        "genre": "Drama, Music",
        "plot": "As a CODA (Child of Deaf Adults), Ruby is the only hearing person in her deaf family. When the family's fishing business is threatened, Ruby finds herself torn between pursuing her love of music and her fear of abandoning her parents."
    },
    {
        "title": "Dune",
        "year": 2021,
        "genre": "Action, Adventure, Sci-Fi",
        "plot": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future."
    },
    {
        "title": "The Power of the Dog",
        "year": 2021,
        "genre": "Drama, Romance, Western",
        "plot": "Charismatic rancher Phil Burbank inspires fear and awe in those around him. When his brother brings home a new wife and her son, Phil torments them until he finds himself exposed to the possibility of love."
    },
    {
        "title": "The French Dispatch",
        "year": 2021,
        "genre": "Comedy, Drama, Romance",
        "plot": "A love letter to journalists set in an outpost of an American newspaper in a fictional twentieth century French city that brings to life a collection of stories published in 'The French Dispatch'."
    },
    {
        "title": "Summer of Soul",
        "year": 2021,
        "genre": "Documentary, Music",
        "plot": "During the same summer as Woodstock, over 300,000 people attended the Harlem Cultural Festival, celebrating African American music and culture, and promoting Black pride and unity. The footage from the festival sat in a basement for 50 years."
    },
    {
        "title": "Belfast",
        "year": 2021,
        "genre": "Biography, Drama",
        "plot": "A young boy and his working-class Belfast family experience the tumultuous late 1960s."
    },
    {
        "title": "No Time to Die",
        "year": 2021,
        "genre": "Action, Adventure, Thriller",
        "plot": "James Bond has left active service. His peace is short-lived when Felix Leiter, an old friend from the CIA, turns up asking for help, leading Bond onto the trail of a mysterious villain armed with dangerous new technology."
    },
    {
        "title": "Spider-Man: No Way Home",
        "year": 2021,
        "genre": "Action, Adventure, Fantasy",
        "plot": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man."
    },
    {
        "title": "Tick, Tick... Boom!",
        "year": 2021,
        "genre": "Biography, Drama, Musical",
        "plot": "On the cusp of his 30th birthday, a promising young theater composer navigates love, friendship and the pressures of life as an artist in New York City."
    },
    {
        "title": "King Richard",
        "year": 2021,
        "genre": "Biography, Drama, Sport",
        "plot": "A look at how tennis superstars Venus and Serena Williams became who they are after the coaching from their father Richard Williams."
    },
    {
        "title": "The Lost Daughter",
        "year": 2021,
        "genre": "Drama",
        "plot": "A woman's beach vacation takes a dark turn when she begins to confront the troubles of her past."
    },
    {
        "title": "Encanto",
        "year": 2021,
        "genre": "Animation, Comedy, Family",
        "plot": "A Colombian teenage girl has to face the frustration of being the only member of her family without magical powers."
    },
    {
        "title": "The Green Knight",
        "year": 2021,
        "genre": "Adventure, Drama, Fantasy",
        "plot": "A fantasy retelling of the medieval story of Sir Gawain and the Green Knight."
    },
    {
        "title": "Drive My Car",
        "year": 2021,
        "genre": "Drama",
        "plot": "A renowned stage actor and director learns to cope with his wife's unexpected passing when he receives an offer to direct a production of Uncle Vanya in Hiroshima."
    },
    {
        "title": "The Worst Person in the World",
        "year": 2021,
        "genre": "Comedy, Drama, Romance",
        "plot": "The chronicles of four years in the life of Julie, a young woman who navigates the troubled waters of her love life and struggles to find her career path, leading her to take a realistic look at who she really is."
    },
    {
        "title": "Licorice Pizza",
        "year": 2021,
        "genre": "Comedy, Drama, Romance",
        "plot": "The story of Alana Kane and Gary Valentine growing up, running around and going through the treacherous navigation of first love in the San Fernando Valley, 1973."
    },
    {
        "title": "Everything Everywhere All at Once",
        "year": 2022,
        "genre": "Action, Adventure, Comedy",
        "plot": "An aging Chinese immigrant is swept up in an insane adventure, where she alone can save the world by exploring other universes connecting with the lives she could have led."
    },
    {
        "title": "Top Gun: Maverick",
        "year": 2022,
        "genre": "Action, Drama",
        "plot": "After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him."
    },
    {
        "title": "The Batman",
        "year": 2022,
        "genre": "Action, Crime, Drama",
        "plot": "When the Riddler, a sadistic serial killer, begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement."
    },
    {
        "title": "Nope",
        "year": 2022,
        "genre": "Horror, Mystery, Sci-Fi",
        "plot": "The residents of a lonely gulch in inland California bear witness to an uncanny and chilling discovery."
    },
    {
        "title": "The Banshees of Inisherin",
        "year": 2022,
        "genre": "Comedy, Drama",
        "plot": "Two lifelong friends find themselves at an impasse when one abruptly ends their relationship, with alarming consequences for both of them."
    },
    {
        "title": "All Quiet on the Western Front",
        "year": 2022,
        "genre": "Action, Drama, War",
        "plot": "A young German soldier's terrifying experiences and distress on the western front during World War I."
    },
    {
        "title": "The Fabelmans",
        "year": 2022,
        "genre": "Drama",
        "plot": "Growing up in post-World War II era Arizona, a young man named Sammy Fabelman discovers a shattering family secret and explores how the power of films can help him see the truth."
    },
    {
        "title": "Decision to Leave",
        "year": 2022,
        "genre": "Crime, Drama, Mystery",
        "plot": "A detective investigating a man's death in the mountains meets the dead man's mysterious wife in the course of his dogged sleuthing."
    },
    {
        "title": "RRR",
        "year": 2022,
        "genre": "Action, Drama",
        "plot": "A fictional history of two legendary revolutionaries' journey away from home before they began fighting for their country in the 1920s."
    },
    {
        "title": "Aftersun",
        "year": 2022,
        "genre": "Drama",
        "plot": "Sophie reflects on the shared joy and private melancholy of a holiday she took with her father twenty years earlier. Memories real and imagined fill the gaps between as she tries to reconcile the father she knew with the man she didn't."
    },
    {
        "title": "The Whale",
        "year": 2022,
        "genre": "Drama",
        "plot": "A reclusive English teacher suffering from severe obesity attempts to reconnect with his estranged teenage daughter for one last chance at redemption."
    },
    {
        "title": "Avatar: The Way of Water",
        "year": 2022,
        "genre": "Action, Adventure, Fantasy",
        "plot": "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home."
    },
    {
        "title": "Tár",
        "year": 2022,
        "genre": "Drama, Music",
        "plot": "Set in the international world of Western classical music, the film centers on Lydia Tár, widely considered one of the greatest living composer-conductors and the very first female director of a major German orchestra."
    },
    {
        "title": "Triangle of Sadness",
        "year": 2022,
        "genre": "Comedy, Drama",
        "plot": "A fashion model celebrity couple join an eventful cruise for the super-rich."
    },
    {
        "title": "Babylon",
        "year": 2022,
        "genre": "Comedy, Drama, History",
        "plot": "A tale of outsized ambition and outrageous excess, it traces the rise and fall of multiple characters during an era of unbridled decadence and depravity in early Hollywood."
    },
    {
        "title": "Glass Onion: A Knives Out Mystery",
        "year": 2022,
        "genre": "Comedy, Crime, Drama",
        "plot": "Famed Southern detective Benoit Blanc travels to Greece for his latest case."
    },
    {
        "title": "Women Talking",
        "year": 2022,
        "genre": "Drama",
        "plot": "Do nothing. Stay and fight. Or leave. In 2010, the women of an isolated religious community grapple with reconciling a brutal reality with their faith."
    },
    {
        "title": "The Menu",
        "year": 2022,
        "genre": "Comedy, Horror, Thriller",
        "plot": "A young couple travels to a remote island to eat at an exclusive restaurant where the chef has prepared a lavish menu, with some shocking surprises."
    },
    {
        "title": "Pearl",
        "year": 2022,
        "genre": "Horror",
        "plot": "In 1918, a young woman on the brink of madness pursues stardom in a desperate attempt to escape the drudgery, isolation and lovelessness of life on her parents' farm."
    },
    {
        "title": "Moonage Daydream",
        "year": 2022,
        "genre": "Documentary, Music",
        "plot": "A cinematic odyssey exploring David Bowie's creative and musical journey. From visionary filmmaker Brett Morgen, and sanctioned by the Bowie estate."
    },
    {
        "title": "Barbie",
        "year": 2023,
        "genre": "Adventure, Comedy, Fantasy",
        "plot": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans."
    },
    {
        "title": "Oppenheimer",
        "year": 2023,
        "genre": "Biography, Drama, History",
        "plot": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II."
    },
    {
        "title": "Killers of the Flower Moon",
        "year": 2023,
        "genre": "Crime, Drama, History",
        "plot": "When oil is discovered in 1920s Oklahoma under Osage Nation land, the Osage people are murdered one by one - until the FBI steps in to unravel the mystery."
    },
    {
        "title": "Past Lives",
        "year": 2023,
        "genre": "Drama, Romance",
        "plot": "Nora and Hae Sung, two deeply connected childhood friends, are wrest apart after Nora's family emigrates from South Korea. Two decades later, they are reunited in New York for one fateful week as they confront notions of destiny and love."
    },
    {
        "title": "The Holdovers",
        "year": 2023,
        "genre": "Comedy, Drama",
        "plot": "A cranky history teacher at a remote prep school is forced to remain on campus over the holidays with a troubled student who has no place to go."
    },
    {
        "title": "Poor Things",
        "year": 2023,
        "genre": "Comedy, Drama, Romance",
        "plot": "The incredible tale about the fantastical evolution of Bella Baxter, a young woman brought back to life by the brilliant and unorthodox scientist Dr. Godwin Baxter."
    },
    {
        "title": "Anatomy of a Fall",
        "year": 2023,
        "genre": "Crime, Drama, Mystery",
        "plot": "A woman is suspected of her husband's murder, and their blind son faces a moral dilemma as the sole witness."
    },
    {
        "title": "Spider-Man: Across the Spider-Verse",
        "year": 2023,
        "genre": "Animation, Action, Adventure",
        "plot": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence. When the heroes clash on how to handle a new threat, Miles must redefine what it means to be a hero."
    },
    {
        "title": "Saltburn",
        "year": 2023,
        "genre": "Comedy, Drama, Thriller",
        "plot": "A student at Oxford University finds himself drawn into the world of a charming and aristocratic classmate, who invites him to his eccentric family's sprawling estate for a summer never to be forgotten."
    },
    {
        "title": "The Zone of Interest",
        "year": 2023,
        "genre": "Drama, History, Thriller",
        "plot": "The commandant of Auschwitz, Rudolf Höss, and his wife Hedwig, strive to build a dream life for their family in a house and garden next to the camp."
    },
    {
        "title": "The Boy and the Heron",
        "year": 2023,
        "genre": "Animation, Adventure, Drama",
        "plot": "A young boy named Mahito, yearning for his mother, ventures into a world shared by the living and the dead. There, death comes to an end, and life finds a new beginning."
    },
    {
        "title": "May December",
        "year": 2023,
        "genre": "Comedy, Drama",
        "plot": "Twenty years after their notorious tabloid romance gripped the nation, a married couple buckles under the pressure when an actress arrives to do research for a film about their past."
    },
    {
        "title": "Godzilla Minus One",
        "year": 2023,
        "genre": "Action, Adventure, Drama",
        "plot": "Post war Japan is at its lowest point when a new crisis emerges in the form of a giant monster, baptized in the horrific power of the atomic bomb."
    },
    {
        "title": "Maestro",
        "year": 2023,
        "genre": "Biography, Drama, Music",
        "plot": "This film tells the complex love story of Leonard Bernstein and Felicia Montealegre Cohn Bernstein, a story that spans over 30 years-from the time they met in 1946 at a party and continuing through two engagements, a 25-year marriage, and three children."
    },
    {
        "title": "Napoleon",
        "year": 2023,
        "genre": "Action, Biography, Drama",
        "plot": "An epic that details the checkered rise and fall of French Emperor Napoleon Bonaparte and his relentless journey to power through the prism of his addictive, volatile relationship with his wife, Josephine."
    },
    {
        "title": "The Color Purple",
        "year": 2023,
        "genre": "Drama, Musical",
        "plot": "A woman named Celie survives incredible abuse and bigotry. Forced into an abusive marriage with a much older man whom she calls 'Mister,' Celie discovers her self-worth through the help of two remarkable women."
    },
    {
        "title": "Guardians of the Galaxy Vol. 3",
        "year": 2023,
        "genre": "Action, Adventure, Comedy",
        "plot": "Still reeling from the loss of Gamora, Peter Quill rallies his team to defend the universe and one of their own - a mission that could mean the end of the Guardians if not successful."
    },
    {
        "title": "John Wick: Chapter 4",
        "year": 2023,
        "genre": "Action, Crime, Thriller",
        "plot": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes."
    },
    {
        "title": "Mission: Impossible - Dead Reckoning Part One",
        "year": 2023,
        "genre": "Action, Adventure, Thriller",
        "plot": "Ethan Hunt and his IMF team must track down a dangerous weapon before it falls into the wrong hands."
    },
    {
        "title": "Asteroid City",
        "year": 2023,
        "genre": "Comedy, Drama, Romance",
        "plot": "Following a writer on his world famous fictional digest as multiple stories begin to intertwine and overlap with one another."
    },
    {
        "title": "Beau Is Afraid",
        "year": 2023,
        "genre": "Comedy, Drama, Horror",
        "plot": "Following a paranoid man who embarks on an epic odyssey to get home to his mother."
    },
    {
        "title": "Talk to Me",
        "year": 2023,
        "genre": "Horror, Thriller",
        "plot": "When a group of friends discover how to conjure spirits using an embalmed hand, they become hooked on the new thrill, until one of them goes too far and unleashes terrifying supernatural forces."
    },
    {
        "title": "The Killer",
        "year": 2023,
        "genre": "Action, Crime, Thriller",
        "plot": "A ruthless assassin on the verge of retirement is on the hunt for anyone who forced him to miss a target."
    },
    {
        "title": "Blue Beetle",
        "year": 2023,
        "genre": "Action, Adventure, Sci-Fi",
        "plot": "An alien scarab chooses Jaime Reyes to be its symbiotic host, giving the Mexican American college graduate an incredible superpowered armor and weaponry."
    },
    {
        "title": "Creed III",
        "year": 2023,
        "genre": "Drama, Sport",
        "plot": "Adonis Creed is thriving in both his career and family life, but when Damian, a childhood friend and former boxing prodigy resurfaces after serving time in prison, he's eager to prove that he deserves his shot in the ring."
    },
    {
        "title": "Dumb Money",
        "year": 2023,
        "genre": "Biography, Comedy, Drama",
        "plot": "The story of two everyday people who fought back against hedge funds and billionaires on Wall Street, and in the process, they both make millions and inspire a worldwide movement against Wall Street."
    },
    {
        "title": "Bottoms",
        "year": 2023,
        "genre": "Comedy, Sport",
        "plot": "Two unpopular queer high school students start a fight club to have sex before graduation."
    },
    {
        "title": "Scream VI",
        "year": 2023,
        "genre": "Horror, Mystery, Thriller",
        "plot": "Four survivors of the Ghostface murders leave Woodsboro behind for a fresh start in New York City. However, they're not safe as the killer reemerges to cause more mayhem."
    }
]

# Additional movie data for a more diverse dataset
ADDITIONAL_MOVIES = [
    {
        "title": "Memento",
        "year": 2000,
        "genre": "Mystery, Thriller",
        "plot": "A man with short-term memory loss attempts to track down his wife's murderer."
    },
    {
        "title": "City of God",
        "year": 2002,
        "genre": "Crime, Drama",
        "plot": "In the slums of Rio, two kids' paths diverge as one struggles to become a photographer and the other a kingpin."
    },
    {
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genre": "Adventure, Comedy, Crime",
        "plot": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge."
    },
    {
        "title": "Whiplash",
        "year": 2014,
        "genre": "Drama, Music",
        "plot": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential."
    },
    {
        "title": "Coco",
        "year": 2017,
        "genre": "Animation, Adventure, Family",
        "plot": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer."
    },
    {
        "title": "The Witch",
        "year": 2015,
        "genre": "Horror, Mystery",
        "plot": "A family in 1630s New England is torn apart by the forces of witchcraft, black magic, and possession."
    },
    {
        "title": "Moonlight",
        "year": 2016,
        "genre": "Drama",
        "plot": "A young African-American man grapples with his identity and sexuality while experiencing the everyday struggles of childhood, adolescence, and burgeoning adulthood."
    },
    {
        "title": "The Farewell",
        "year": 2019,
        "genre": "Comedy, Drama",
        "plot": "A Chinese family discovers their grandmother has only a short while left to live and decide to keep her in the dark, scheduling a wedding to gather before she dies."
    },
    {
        "title": "Nomadland",
        "year": 2020,
        "genre": "Drama",
        "plot": "After losing everything in the Great Recession, a woman embarks on a journey through the American West, living as a van-dwelling modern-day nomad."
    },
    {
        "title": "Soul",
        "year": 2020,
        "genre": "Animation, Adventure, Comedy",
        "plot": "After landing the gig of a lifetime, a New York jazz pianist suddenly finds himself trapped in a strange land between Earth and the afterlife."
    },
    {
        "title": "The Father",
        "year": 2020,
        "genre": "Drama",
        "plot": "A man refuses all assistance from his daughter as he ages. As he tries to make sense of his changing circumstances, he begins to doubt his loved ones, his own mind and even the fabric of his reality."
    },
    {
        "title": "Sound of Metal",
        "year": 2019,
        "genre": "Drama, Music",
        "plot": "A heavy-metal drummer's life is thrown into freefall when he begins to lose his hearing."
    },
    {
        "title": "Minari",
        "year": 2020,
        "genre": "Drama",
        "plot": "A Korean family starts a farm in 1980s Arkansas."
    },
    {
        "title": "Promising Young Woman",
        "year": 2020,
        "genre": "Crime, Drama, Thriller",
        "plot": "A young woman, traumatized by a tragic event in her past, seeks out vengeance against those who crossed her path."
    },
    {
        "title": "Palm Springs",
        "year": 2020,
        "genre": "Comedy, Fantasy, Romance",
        "plot": "Stuck in a time loop, two wedding guests develop a budding romance while living the same day over and over again."
    },
    {
        "title": "The Lighthouse",
        "year": 2019,
        "genre": "Drama, Fantasy, Horror",
        "plot": "Two lighthouse keepers try to maintain their sanity while living on a remote and mysterious New England island in the 1890s."
    },
    {
        "title": "Uncut Gems",
        "year": 2019,
        "genre": "Crime, Drama, Thriller",
        "plot": "With his debts mounting and angry collectors closing in, a fast-talking New York City jeweler risks everything in hope of staying afloat and alive."
    },
    {
        "title": "Little Women",
        "year": 2019,
        "genre": "Drama, Romance",
        "plot": "Jo March reflects back and forth on her life, telling the beloved story of the March sisters - four young women, each determined to live life on her own terms."
    },
    {
        "title": "Marriage Story",
        "year": 2019,
        "genre": "Comedy, Drama, Romance",
        "plot": "Noah Baumbach's incisive and compassionate look at a marriage breaking up and a family staying together."
    },
    {
        "title": "Portrait of a Lady on Fire",
        "year": 2019,
        "genre": "Drama, Romance",
        "plot": "On an isolated island in Brittany at the end of the eighteenth century, a female painter is obliged to paint a wedding portrait of a young woman."
    },
]

# Combine movie lists
all_movies = MOVIES + ADDITIONAL_MOVIES

# Deduplicate movies by title
unique_movies = {}
for movie in all_movies:
    if movie["title"] not in unique_movies:
        unique_movies[movie["title"]] = movie

# Convert back to list
deduplicated_movies = list(unique_movies.values())

# Print genre distribution
current_genre_count = defaultdict(int)
for movie in deduplicated_movies:
    genres = movie["genre"].split(", ")
    for genre in genres:
        current_genre_count[genre] += 1

print(f"Generated {len(deduplicated_movies)} unique movies")
print("\nGenre distribution:")
for genre, count in sorted(current_genre_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{genre}: {count} movies")

# Write to CSV
output_path = "../static/data/movies.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["title", "year", "genre", "plot"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    for movie in deduplicated_movies:
        writer.writerow(movie)

print(f"\nMovie data written to {output_path}")