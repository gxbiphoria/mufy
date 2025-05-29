import streamlit as st
import random # For skill checks

# --- Session State Initialization ---
# This block ensures that all necessary game variables are initialized
# when the app first runs or when the session state is cleared (e.g., on restart).
if 'inventory' not in st.session_state:
    st.session_state.inventory = [] # List to store collected items
if 'romance' not in st.session_state:
    st.session_state.romance = None # Stores the name of the chosen romance interest (Alex, Jordan, Taylor)
if 'fashion_score' not in st.session_state:
    st.session_state.fashion_score = 'Medium' # Can be 'Low', 'Medium', 'High'
if 'relationship_scores' not in st.session_state:
    # Dictionary to store relationship scores (0-5 scale) for key characters.
    # Maya is a new character added here.
    st.session_state.relationship_scores = {'Alex': 0, 'Jordan': 0, 'Taylor': 0, 'Blake': 0, 'Maya': 0}
if 'clues_collected' not in st.session_state:
    st.session_state.clues_collected = [] # List of unique clues found (for tracking progress)
if 'story_progress' not in st.session_state:
    st.session_state.story_progress = 0 # 0-100 percentage, reflecting scene progression
if 'date_opportunity_taken' not in st.session_state:
    st.session_state.date_opportunity_taken = False # Tracks if the romance interlude was taken
if 'final_romance_dialogue_unlocked' not in st.session_state:
    st.session_state.final_romance_dialogue_unlocked = False # Special flag for maxed romance dialogue
if 'interlude_response_message' not in st.session_state:
    st.session_state.interlude_response_message = "" # Stores messages from romance interlude for next scene
if 'player_observant' not in st.session_state:
    st.session_state.player_observant = 0 # Player hidden stat for observation checks (increases with certain choices)
if 'social_grace' not in st.session_state:
    st.session_state.social_grace = 0 # Player hidden stat for social interactions (increases with certain choices)
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'Normal' # Default difficulty setting

# --- Navigation Setup ---
# Get current scene and choice from Streamlit's query parameters.
# 'arrival' is the default starting scene if no parameters are present.
params = st.query_params
scene = params.get('scene', 'arrival')
choice = params.get('choice', None)

# --- Difficulty Adjustment ---
# The difficulty can only be set at the very beginning of the game (arrival scene).
if scene == 'arrival':
    st.sidebar.header("Game Settings")
    st.session_state.difficulty = st.sidebar.selectbox(
        "Select Difficulty:",
        ('Easy', 'Normal', 'Hard'),
        # Set the default selection based on the current session state difficulty
        index=('Easy', 'Normal', 'Hard').index(st.session_state.difficulty)
    )
    st.sidebar.write(f"Difficulty: {st.session_state.difficulty}")

# Adjust game parameters based on chosen difficulty.
# These multipliers and thresholds will affect skill checks and relationship gains.
skill_check_threshold = 3 # Default for Normal difficulty (e.g., need random.randint(1,5) >= 3)
relationship_gain_multiplier = 1 # Default for Normal
clue_chance_multiplier = 1 # Default for Normal

if st.session_state.difficulty == 'Easy':
    skill_check_threshold = 2 # Easier skill checks
    relationship_gain_multiplier = 1.5 # Faster relationship gains
    clue_chance_multiplier = 1.2 # Higher chance to find clues
elif st.session_state.difficulty == 'Hard':
    skill_check_threshold = 4 # Harder skill checks
    relationship_gain_multiplier = 0.5 # Slower relationship gains
    clue_chance_multiplier = 0.8 # Lower chance to find clues

# --- Scene Titles ---
# A dictionary mapping scene IDs to their display titles.
titles = {
    'arrival': "🏰 Arrival at the Grand Runway Mansion",
    'pre_challenge_mingling': "🥂 Pre-Challenge Mingling", # New scene
    'design_challenge': "🎨 Midnight Rebellion Challenge",
    'backstage_incident': "🎭 Backstage Incident",
    'rooftop_party': "🌆 Rooftop Revelations",
    'romance_interlude': "💖 A Moment Together",
    'midnight_ball': "💃 Midnight Masquerade Ball",
    'secret_passage': "🔍 Secret Passage Discovery",
    'hidden_study': "📚 The Hidden Study", # Expanded and renamed from secret_passage_details
    'marcelline_trap': "덫 Marcelline's Trap", # New scene
    'confrontation': "⚡ The Final Showdown"
}

# --- Game Status Sidebar ---
# This section displays the player's current stats, inventory, and progress.
st.sidebar.title("Game Status")

st.sidebar.header("Your Stats")
st.sidebar.write(f"**Fashion Score:** {st.session_state.fashion_score}")
st.sidebar.write(f"**Observant:** {st.session_state.player_observant}") # Display new stat
st.sidebar.write(f"**Social Grace:** {st.session_state.social_grace}") # Display new stat

st.sidebar.header("Relationships")
for character, score in st.session_state.relationship_scores.items():
    st.sidebar.write(f"**{character}:** {score} / 5")
    if st.session_state.romance == character:
        st.sidebar.write(f"*(Romantic Interest)*") # Indicate chosen romance interest

st.sidebar.header("Inventory")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.sidebar.write(f"- {item}")
else:
    st.sidebar.write("Empty")

st.sidebar.header("Clues Collected")
if st.session_state.clues_collected:
    for clue in st.session_state.clues_collected:
        st.sidebar.write(f"- {clue}")
else:
    st.sidebar.write("None yet...")

st.sidebar.header("Story Progress")
st.sidebar.progress(st.session_state.story_progress / 100)
st.sidebar.write(f"{st.session_state.story_progress}% Complete")

# Set the main page title dynamically based on the current scene.
st.title(titles.get(scene, "Fashion Fatal"))

# --- Story Scenes Implementation ---

# Scene: Arrival at the Grand Runway Mansion
if scene == 'arrival':
    st.session_state.story_progress = 5 # Adjusted progress for new early scene
    st.write("The Grand Runway Mansion looms ahead, its grandeur veiled by a thin mist. Ivy creeps along marble columns, and golden lanterns flicker in the twilight. A black iron gate groans open as your car glides into the circular drive, tires crunching on gravel. Fashion royalty strides up the steps in stilettos and sharp suits. Cameras flash—you’re not just here to design; you’re here to survive.")
    st.write("Inside, the foyer stretches wide with a sweeping staircase, red velvet runners leading to polished floors. Crystal chandeliers cast rainbows across silk-draped walls. Contestants gather near a marble bar, whispering, sizing each other up.")
    st.write("A tall figure in a crisp suit—Taylor, the butler—approaches with a silver tray of champagne flutes.")
    st.write('"Welcome to the Grand Runway Mansion. I am Taylor, the butler. Should you require anything during your stay, do not hesitate to ask." His gaze lingers for a moment, a hint of something unreadable in his eyes.')

    st.write("\n**What is your immediate focus?**")
    # Choices leading to the new 'pre_challenge_mingling' scene.
    st.button('Mingle with other contestants.', on_click=lambda: st.query_params.update({'scene': 'pre_challenge_mingling', 'choice': 'mingle_initial'}))
    st.button('Observe your surroundings closely.', on_click=lambda: st.query_params.update({'scene': 'pre_challenge_mingling', 'choice': 'observe_initial'}))
    st.button('Seek out the most influential person.', on_click=lambda: st.query_params.update({'scene': 'pre_challenge_mingling', 'choice': 'seek_influential'}))

# NEW SCENE: Pre-Challenge Mingling
elif scene == 'pre_challenge_mingling':
    st.session_state.story_progress = 10
    if choice == 'mingle_initial':
        st.session_state.social_grace += 1 # Increase social grace
        st.write('You circulate, exchanging pleasantries with a few lesser-known designers. You get a feel for the room\'s atmosphere, though no major connections are made yet.')
    elif choice == 'observe_initial':
        st.session_state.player_observant += 1 # Increase observant stat
        # Player gains initial clues if they haven't already.
        if '📜 Faded Invitation' not in st.session_state.inventory:
            st.session_state.inventory.append('📜 Faded Invitation')
            st.session_state.clues_collected.append('Faded Invitation to Patron\'s Soiree')
        st.write('You discreetly wander towards a forgotten corner, behind a large potted palm. Tucked away, you find a **📜 Faded Invitation** to an "Exclusive Patron\'s Soiree" from years ago, with "East Wing" scrawled on the back in a different hand. It feels strangely significant.')
        if '♟️ Chess Piece (Knight)' not in st.session_state.inventory:
            st.session_state.inventory.append('♟️ Chess Piece (Knight)')
            st.session_state.clues_collected.append('Chess Piece (Knight)')
        st.write('You also notice a peculiar **♟️ Chess Piece** [Knight] on a side table – it looks like it\'s been moved recently. You pick it up, feeling a faint chill.')
    elif choice == 'seek_influential':
        st.session_state.social_grace += 1 # Increase social grace
        st.write('You make eye contact with a few established names, but they seem preoccupied. Alex, however, catches your gaze and offers a confident smile. You feel a pull towards them.')

    st.write("\n---")
    st.write("The murmuring continues. Now, who do you approach to make a more significant impression?")

    # Choices to approach main characters, leading to the design challenge.
    st.button('Approach **Alex**: The Charismatic Rival', on_click=lambda: st.query_params.update({'scene': 'design_challenge', 'choice': 'alex_arrival'}))
    st.button('Approach **Jordan**: The Quiet Observer', on_click=lambda: st.query_params.update({'scene': 'design_challenge', 'choice': 'jordan_arrival'}))
    st.button('Observe **Taylor**: The Enigmatic Butler', on_click=lambda: st.query_params.update({'scene': 'design_challenge', 'choice': 'taylor_arrival'}))
    st.button('Approach **Maya**: The Spirited Newcomer', on_click=lambda: st.query_params.update({'scene': 'design_challenge', 'choice': 'maya_arrival'})) # New character interaction

# Scene: Design Challenge
elif scene == 'design_challenge':
    st.session_state.story_progress = 25
    # Initial character interactions and relationship score adjustments based on choice.
    if choice == 'alex_arrival':
        st.session_state.romance = 'Alex'
        st.session_state.relationship_scores['Alex'] += (1 * relationship_gain_multiplier)
        st.write('You approach Alex, who smiles, a flash of white teeth. "Not at all. Always room for one more in the spotlight. Though I prefer to *be* the spotlight." They wink, their confidence almost intimidating.')
    elif choice == 'jordan_arrival':
        st.session_state.romance = 'Jordan'
        st.session_state.relationship_scores['Jordan'] += (1 * relationship_gain_multiplier)
        st.write('Jordan, sketching furiously in a notebook, looks up, eyes cautious. "May the best designer win," they murmur, quickly looking back down. They seem shy, or perhaps, secretive.')
    elif choice == 'taylor_arrival':
        st.session_state.romance = 'Taylor'
        st.session_state.relationship_scores['Taylor'] += (1 * relationship_gain_multiplier)
        st.write('You observe Taylor from a distance. He seems to be watching *everyone*, his expression unreadable. As he notices your gaze, he offers a slight, almost imperceptible nod. You feel a strange sense of intrigue.')
    elif choice == 'maya_arrival': # New character interaction
        st.session_state.relationship_scores['Maya'] += (1 * relationship_gain_multiplier)
        st.write('You approach Maya, who grins, bright and open. "Hey! Glad to see another fresh face. This whole competition is wild, right? Trying to figure out where everyone stands." She seems eager to connect.')

    st.write("\n---")
    st.write('Suddenly, the grand doors swing open, and a figure in a dazzling, avant-garde gown sweeps into the foyer. It’s Marcelline, the enigmatic host and head judge, her eyes sharp, missing nothing.')

    # Marcelline's dynamic dialogue based on your initial fashion score.
    if st.session_state.fashion_score == 'High':
        st.write('Marcelline\'s gaze lingers on your attire, a flicker of grudging respect in her sharp eyes. "You clearly understand presentation," she purrs, "let\'s see if your talent matches your style."')
    elif st.session_state.fashion_score == 'Medium':
        st.write('Marcelline offers a polite but cool nod. "Welcome. I expect nothing less than brilliance."')
    else:
        st.write('Marcelline barely spares you a glance, her focus already on the more established designers. "Don\'t waste my time," she says, dismissively.')

    st.write('Marcelline: "Welcome, designers, to your first challenge. Tonight’s theme is **Midnight Rebellion**. You have three hours to create a look that screams defiance, yet retains elegance. Impress me—or face elimination." Her voice is smooth as silk, but with an underlying steel.')

    st.write("\n**How do you approach the challenge?**")
    # Choices for the design challenge, affecting fashion score or leading to clues.
    st.button('Focus on a daring, creative outfit to impress Marcelline.', on_click=lambda: st.query_params.update({'scene': 'backstage_incident', 'choice': 'creative_design'}))
    st.button('Observe your rivals, looking for weaknesses or inspiration.', on_click=lambda: st.query_params.update({'scene': 'backstage_incident', 'choice': 'spy_rivals'}))
    st.button('Try to subtly charm the judges during the design process.', on_click=lambda: st.query_params.update({'scene': 'backstage_incident', 'choice': 'charm_judges'}))
    if '📜 Faded Invitation' in st.session_state.inventory:
        st.button('Consider the East Wing clue from the invitation.', on_click=lambda: st.query_params.update({'scene': 'backstage_incident', 'choice': 'investigate_east_wing_early'}))

# Scene: Backstage Incident
elif scene == 'backstage_incident':
    st.session_state.story_progress = 40
    # Outcomes of choices from the design challenge.
    if choice == 'creative_design':
        st.session_state.fashion_score = 'High'
        st.write('You pour all your energy into a truly groundbreaking design. As you work, you notice Taylor pass by, his gaze lingering on your progress. He offers a quiet observation: "An intriguing design. Just be cautious. Not everyone here plays fair." You feel a sense of unease.')
    elif choice == 'spy_rivals':
        st.session_state.player_observant += 1 # Increase observant stat
        # Skill check for finding the suspicious photo, influenced by observant stat and difficulty.
        if random.randint(1,5) <= (skill_check_threshold + st.session_state.player_observant):
            if '📱 Suspicious Photo' not in st.session_state.inventory:
                st.session_state.inventory.append('📱 Suspicious Photo')
                st.session_state.clues_collected.append('Suspicious Photo (Blake)')
            st.write('While pretending to sketch, you keep an eye on the other designers. You catch Blake, another contestant, fumbling with Jennifer\'s fabric, a sly look on their face. You manage to snap a **📱 Suspicious Photo** of them moments before Jennifer\'s gown is torn.')
        else:
            st.write('You try to observe your rivals, but the chaos of the design studio makes it difficult. You don\'t catch anything specific.')
    elif choice == 'charm_judges':
        st.session_state.social_grace += 1 # Increase social grace stat
        st.session_state.fashion_score = 'Medium'
        st.write('You spend some time making polite conversation with the assistant judges. Marcelline, however, remains aloof. "Hmm. Promising," she says, her eyes narrowing slightly. "But rebellion isn’t just a look—it’s a mindset."')
    elif choice == 'investigate_east_wing_early':
        st.write('You try to discreetly slip towards the East Wing, but Taylor intercepts you. "The East Wing is off-limits, I\'m afraid," he says, his voice polite but firm. "For your safety, I must insist you return to the design studio." You realize he\'s always watching.')

    st.write("\n---")
    st.write('Suddenly, a gasp echoes through the studio. Jennifer, a fellow contestant, collapses by her workstation, her vibrant gown—hours of painstaking work—now a tattered mess. Someone clearly sabotaged it.')

    st.write("\n**What do you do?**")
    # Choices reacting to the sabotage incident.
    st.button('Rush to help Jennifer rebuild her gown, offering your expertise.', on_click=lambda: st.query_params.update({'scene': 'rooftop_party', 'choice': 'help_jennifer'}))
    st.button('Focus on your own design, maintaining a competitive edge.', on_click=lambda: st.query_params.update({'scene': 'rooftop_party', 'choice': 'focus_self'}))
    st.button('Privately ask Taylor for his observations or help.', on_click=lambda: st.query_params.update({'scene': 'rooftop_party', 'choice': 'ask_taylor_incident'}))
    if '📱 Suspicious Photo' in st.session_state.inventory:
        st.button('Confront Blake directly about the sabotage.', on_click=lambda: st.query_params.update({'scene': 'rooftop_party', 'choice': 'confront_blake_sabotage'}))
    st.button('Seek Maya\'s perspective on the incident.', on_click=lambda: st.query_params.update({'scene': 'rooftop_party', 'choice': 'ask_maya_incident'})) # New interaction

# Scene: Rooftop Party
elif scene == 'rooftop_party':
    st.session_state.story_progress = 55
    # Outcomes of choices from the backstage incident.
    if choice == 'help_jennifer':
        if '🧷 Broken Bracelet' not in st.session_state.inventory:
            st.session_state.inventory.append('🧷 Broken Bracelet')
            st.session_state.clues_collected.append('Broken Bracelet (Jennifer\'s)')
        st.write('You work tirelessly with Jennifer. She\'s visibly touched, offering you a small, grateful smile. "Thank you," she whispers, pressing a delicate **🧷 Broken Bracelet** into your hand. "This was my grandmother\'s. It\'s a good luck charm... maybe it\'ll help you." Your fashion score increases slightly for your compassion.')
        st.session_state.fashion_score = 'High' if st.session_state.fashion_score == 'Medium' else st.session_state.fashion_score
        st.session_state.relationship_scores['Jennifer'] = st.session_state.relationship_scores.get('Jennifer', 0) + (1 * relationship_gain_multiplier)
    elif choice == 'focus_self':
        st.write('You maintain your distance, focusing solely on your final touches. Jennifer looks dejected, but you secure your own performance. Your fashion score is unaffected, but you notice some contestants eyeing you coldly.')
    elif choice == 'ask_taylor_incident':
        st.session_state.relationship_scores['Taylor'] += (1 * relationship_gain_multiplier)
        st.write('Taylor listens patiently, his expression unreadable. "Of course. I am aware of the incident," he says, his voice low. "But be careful whom you trust. Appearances can be deceiving in this mansion." He gives you a knowing look, as if inviting you to dig deeper.')
    elif choice == 'confront_blake_sabotage':
        st.session_state.relationship_scores['Blake'] -= (1 * relationship_gain_multiplier) # Relationship might decrease for confrontation
        # Skill check for successful confrontation, influenced by social grace and difficulty.
        if random.randint(1,5) <= (skill_check_threshold + st.session_state.social_grace):
            st.write('You pull Blake aside, showing them the photo. They blanch, their bravado faltering. "Alright, alright! I was just... sending a message. But Marcelline... she makes us do things. She threatened my family\'s business if I didn\'t play along!" This revelation is startling.')
            if '📝 Blake\'s Confession' not in st.session_state.inventory:
                st.session_state.inventory.append('📝 Blake\'s Confession')
                st.session_state.clues_collected.append('Blake\'s Confession (Marcelline\'s manipulation)')
            st.write('You\'ve gained **📝 Blake\'s Confession** about Marcelline\'s manipulation.')
        else:
            st.write('You try to confront Blake, but they deflect your accusations, becoming defensive and walking away. You sense their guilt but couldn\'t prove it.')
    elif choice == 'ask_maya_incident': # New interaction
        st.session_state.relationship_scores['Maya'] += (1 * relationship_gain_multiplier)
        # Skill check for Maya to reveal information, influenced by social grace.
        if random.randint(1,5) <= (skill_check_threshold + st.session_state.social_grace):
            st.write('Maya sighs, looking around nervously. "I... I think I saw Blake near Jennifer\'s station just before. They seemed really agitated. Marcelline has everyone on edge. She even offered me a \'deal\' to mess with someone else\'s design, but I refused. It felt wrong."')
            if '📜 Maya\'s Observation' not in st.session_state.inventory:
                st.session_state.inventory.append('📜 Maya\'s Observation')
                st.session_state.clues_collected.append('Maya\'s Observation (Blake & Marcelline)')
            st.write('You gain **📜 Maya\'s Observation**.')
        else:
            st.write('Maya just shrugs, "I don\'t know. This whole thing is crazy. Everyone\'s so stressed." She seems unwilling to share more, perhaps out of fear.')

    st.write("\n---")
    st.write('Under a velvet sky, the rooftop glows with fairy lights and soft music. Contestants sip champagne, some celebrating, others still reeling from the challenge. The tension is palpable, but beneath it, a sense of opportunity.')

    st.write("\n**What do you do now?**")
    # Offer a date opportunity if romance interest is chosen and not taken.
    if st.session_state.romance and not st.session_state.date_opportunity_taken:
        st.button(f'Spend private time with **{st.session_state.romance}**.', on_click=lambda: st.query_params.update({'scene': 'romance_interlude', 'choice': f'romance_interlude_{st.session_state.romance.lower()}'}))

    # Options to interact with characters or eavesdrop, leading to Midnight Ball.
    st.button('Seek out **Alex**, who seems to be holding court.', on_click=lambda: st.query_params.update({'scene': 'midnight_ball', 'choice': 'talk_alex_party'}))
    st.button('Approach **Jordan**, who looks lost in thought.', on_click=lambda: st.query_params.update({'scene': 'midnight_ball', 'choice': 'approach_jordan_party'}))
    st.button('Observe **Taylor**, always in the background.', on_click=lambda: st.query_params.update({'scene': 'midnight_ball', 'choice': 'observe_taylor_party'}))
    st.button('Eavesdrop on conversations, looking for gossip or clues.', on_click=lambda: st.query_params.update({'scene': 'midnight_ball', 'choice': 'eavesdrop_party'}))
    st.button('Talk to **Maya**, she might have more to share.', on_click=lambda: st.query_params.update({'scene': 'midnight_ball', 'choice': 'talk_maya_party'})) # New interaction

# NEW SCENE: Romance Interlude
elif scene == 'romance_interlude':
    st.session_state.story_progress = 60 # Slightly higher progress for this dedicated scene
    st.session_state.date_opportunity_taken = True # Mark as taken

    # Logic for Alex's date, affecting relationship score and providing dialogue.
    if choice == 'romance_interlude_alex':
        st.session_state.relationship_scores['Alex'] += (2 * relationship_gain_multiplier)
        st.write('You and Alex slip away to a secluded balcony overlooking the city lights. Alex leans against the railing, the soft glow illuminating their profile.')
        st.write('"This competition... it\'s a game, and I play to win," Alex murmurs, turning to you. "But with you, it feels different. Less like a game, more like... a discovery. You have an edge, a fire. Tell me, what truly drives you?"')
        st.write("\n**How do you respond?**")

        if st.button('Confess your suspicion about Marcelline and the mansion.'):
            st.session_state.relationship_scores['Alex'] += (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Alex\'s eyes gleam. "Intriguing. I knew there was more to you than met the eye. Perhaps we can unravel this mystery... together." Your bond deepens, and Alex seems genuinely interested in assisting you.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})
        if st.button('Talk about your passion for design and the future you envision.'):
            st.session_state.relationship_scores['Alex'] += (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Alex smiles warmly. "A true artist. I admire your vision. Perhaps our futures are more intertwined than we realize." You feel a strong, shared ambition.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})
        if st.button('Dodge the question, keeping your cards close.'):
            st.session_state.relationship_scores['Alex'] -= (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Alex\'s smile falters slightly. "Fair enough. Some mysteries are best left unsolved... for now." You sense a slight distance in their demeanor.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})

    # Logic for Jordan's date.
    elif choice == 'romance_interlude_jordan':
        st.session_state.relationship_scores['Jordan'] += (2 * relationship_gain_multiplier)
        st.write('You find Jordan sketching in a quiet corner of the mansion\'s library, surrounded by ancient tomes. They look up, startled, but then offer a small, shy smile.')
        st.write('"I always find solace in stories," Jordan says softly, closing their notebook. "Especially the ones that aren\'t easily told. This mansion... it holds many. What kinds of stories do you seek here?"')
        st.write("\n**How do you respond?**")

        if st.button('Admit you\'re looking for answers about the mansion\'s past.'):
            st.session_state.relationship_scores['Jordan'] += (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Jordan\'s eyes widen in understanding. "I felt it too. A hidden history. Perhaps we can uncover it, piece by piece." They seem relieved to share this burden with you.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})
        if st.button('Share a personal story about why fashion is important to you.'):
            st.session_state.relationship_scores['Jordan'] += (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Jordan listens intently, their expression softening. "Your journey is beautiful. It reminds me that even quiet stories can hold immense power." You feel a deep, empathetic connection.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})
        if st.button('Change the subject, asking about their sketches.'):
            st.session_state.relationship_scores['Jordan'] -= (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Jordan nods, but their eyes hold a flicker of disappointment. They seem to retreat into themselves slightly.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})

    # Logic for Taylor's date.
    elif choice == 'romance_interlude_taylor':
        st.session_state.relationship_scores['Taylor'] += (2 * relationship_gain_multiplier)
        st.write('Taylor leads you to a rarely used conservatory, filled with exotic plants and the scent of night-blooming jasmine. He offers you a quiet, knowing smile.')
        st.write('"This mansion has seen many secrets bloom and wither," Taylor says, his voice a low, calming murmur. "I have merely been its silent keeper. But sometimes, a keeper yearns for a confidant. Tell me, what troubles your mind most about this place?"')
        st.write("\n**How do you respond?**")

        if st.button('Express your fear of Marcelline\'s true nature and the hidden dangers.'):
            st.session_state.relationship_scores['Taylor'] += (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Taylor nods gravely. "Your instincts serve you well. She is indeed dangerous. Knowing you are aware, it... gives me hope. I will protect you." You feel a surge of trust and protection.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})
        if st.button('Ask about his long history with the mansion and Marcelline.'):
            st.session_state.relationship_scores['Taylor'] += (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Taylor\'s gaze softens. "A long story, and one I may share, in time. For now, know that my loyalty lies with what is just. And with you." You sense a profound loyalty in him.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})
        if st.button('Keep your concerns vague, maintaining some distance.'):
            st.session_state.relationship_scores['Taylor'] -= (1 * relationship_gain_multiplier)
            st.session_state.interlude_response_message = 'Taylor\'s expression remains impassive, but you feel a subtle shift, a hint of his previous reserve returning.'
            st.query_params.update({'scene': 'midnight_ball', 'choice': 'after_interlude'})

    # Display the stored message after the choice is made and the page reruns.
    if st.session_state.interlude_response_message:
        st.write(st.session_state.interlude_response_message)
        # Message is cleared in the next scene for better visibility.

    st.write("\n---")
    st.write('After your private moment, you feel a deeper connection to your chosen companion and return to the main party.')

# Scene: Midnight Ball
elif scene == 'midnight_ball':
    st.session_state.story_progress = 70
    # Process message from interlude if applicable.
    if st.session_state.interlude_response_message:
        st.write(st.session_state.interlude_response_message)
        st.session_state.interlude_response_message = "" # Clear after displaying

    # Dynamic dialogue based on whether the romance interlude was taken.
    if st.session_state.date_opportunity_taken:
        st.write('Having had a private moment, you feel a renewed sense of purpose and connection as the Midnight Ball begins to truly unfold.')
        if choice == 'after_interlude' and st.session_state.romance:
            st.write(f"Your recent conversation with {st.session_state.romance} echoes in your mind, strengthening your resolve.")

        st.write("\n---")
        st.write('A masked ball unfolds under candlelight. Marcelline descends the grand staircase, her gown shimmering, her smile chilling. "Enjoy the festivities, my dears," she announces, her eyes sweeping over the crowd, lingering on you for a moment too long.')
    else: # Original flow if no interlude was taken.
        # Logic for talking to characters if no interlude was taken.
        if choice == 'talk_alex_party':
            st.write('You talk to Alex, who is surrounded by admirers. They are charming but evasive. "Just enjoying the spectacle," they say, brushing off your questions about Marcelline. "Best not to poke the bear, darling."')
        elif choice == 'approach_jordan_party':
            st.session_state.relationship_scores['Jordan'] += (2 * relationship_gain_multiplier)
            st.write('Jordan, still sketching, seems more relaxed tonight. They glance around nervously before confiding, "The Patron is not what she seems. I\'ve seen her in the East Wing, always late at night. There\'s something there... something hidden. Be vigilant." They slip you a crumpled napkin with a crude map. Your bond with Jordan strengthens.')
            if '🗺️ Jordan\'s Map' not in st.session_state.inventory:
                st.session_state.inventory.append('🗺️ Jordan\'s Map')
                st.session_state.clues_collected.append('Jordan\'s Map (East Wing)')
        elif choice == 'observe_taylor_party':
            st.session_state.relationship_scores['Taylor'] += (2 * relationship_gain_multiplier)
            st.write('You find Taylor by the bar, calmly polishing glasses. He looks up as you approach, a rare, gentle smile on his face. "Looking for answers, are we?" he asks, his voice soft. "The Patron has many secrets. Her past is intertwined with this very mansion. Look for the unusual... in the East Wing, perhaps." He subtly points to a seemingly innocuous tapestry. Your connection with Taylor deepens.')
            if '🗝️ Tarnished Key' not in st.session_state.inventory:
                st.session_state.inventory.append('🗝️ Tarnished Key')
                st.session_state.clues_collected.append('Tarnished Key (Taylor\'s clue)')
            st.write('As he walks away, you notice a small, **🗝️ Tarnished Key** resting on the bar where he stood. It feels ancient.')
        elif choice == 'eavesdrop_party':
            st.session_state.player_observant += 1 # Increase observant stat
            # Skill check for eavesdropping, influenced by observant stat and difficulty.
            if random.randint(1,5) <= (skill_check_threshold + st.session_state.player_observant):
                if '🤫 Gossip Snippet' not in st.session_state.inventory:
                    st.session_state.inventory.append('🤫 Gossip Snippet')
                    st.session_state.clues_collected.append('Gossip Snippet (Marcelline\'s past)')
                st.write('You overhear a fragment of conversation between two minor designers: "Marcelline bought this mansion cheap... something about the old owner just vanishing. And those rumors about her previous competition... unsettling." You gain a **🤫 Gossip Snippet**.')
            else:
                st.write('You try to eavesdrop, but the music is too loud and the conversations are too fragmented to understand anything useful.')
        elif choice == 'talk_maya_party': # New interaction
            st.session_state.relationship_scores['Maya'] += (1 * relationship_gain_multiplier)
            # Skill check for Maya to reveal the cryptic note, influenced by social grace.
            if random.randint(1,5) <= (skill_check_threshold + st.session_state.social_grace):
                st.write('Maya pulls you aside, her expression serious. "I found this earlier," she whispers, pressing a **📜 Cryptic Note** into your hand. "It was tucked into a book about the mansion\'s history. It talks about a \'secret patron\' and a \'legacy of shadows.\' It freaked me out, but maybe it means something to you."')
                if '📜 Cryptic Note' not in st.session_state.inventory:
                    st.session_state.inventory.append('📜 Cryptic Note')
                    st.session_state.clues_collected.append('Cryptic Note (Secret Patron)')
            else:
                st.write('Maya is friendly, but she seems distracted by the party. She doesn\'t offer any new information.')

        st.write("\n---")
        st.write('A masked ball unfolds under candlelight. Marcelline descends the grand staircase, her gown shimmering, her smile chilling. "Enjoy the festivities, my dears," she announces, her eyes sweeping over the crowd, lingering on you for a moment too long.')

    st.write("\n**What is your next move?**")
    # Choices leading to the secret passage or further investigation.
    st.button('Sneak into the VIP Area, where Marcelline is heading.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'sneak_vip'}))
    st.button('Observe Marcelline and Alex closely from a distance.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'observe_marcelline_alex'}))
    # Option to find East Wing if relevant clues are held.
    if any(clue in st.session_state.inventory for clue in ['🗺️ Jordan\'s Map', '🗝️ Tarnished Key', '📜 Faded Invitation', '♟️ Chess Piece (Knight)', '📜 Cryptic Note']):
        st.button('Attempt to find the East Wing entrance based on your clues.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'find_east_wing_clue'}))
    if '📝 Blake\'s Confession' in st.session_state.inventory:
        st.button('Try to talk to Blake again, press for more information.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'press_blake'}))
    # Options to examine collected items for more clues.
    if '♟️ Chess Piece (Knight)' in st.session_state.inventory:
        st.button('Examine the Chess Piece you found.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'examine_chess_piece'}))
    if '🧷 Broken Bracelet' in st.session_state.inventory:
        st.button('Examine the Broken Bracelet for any hidden meaning.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'examine_bracelet'}))


# Scene: Secret Passage Discovery (Entry point to East Wing)
elif scene == 'secret_passage':
    st.session_state.story_progress = 75 # Adjusted progress for new scene
    
    # Flag to control if the general options for finding evidence are shown.
    show_general_secret_passage_options = True

    if choice == 'sneak_vip':
        # Chance to find coded letter, influenced by clue chance multiplier.
        if random.random() < (0.6 * clue_chance_multiplier): # 60% base chance
            if '✉️ Coded Letter' not in st.session_state.inventory:
                st.session_state.inventory.append('✉️ Coded Letter')
                st.session_state.clues_collected.append('Coded Letter (Benefactor)')
            st.write('You manage to slip past the VIP security. Inside, you find Marcelline speaking in hushed tones with an unknown figure. As they leave, you notice a **✉️ Coded Letter** dropped on the floor, its contents unsettlingly cryptic.')
        else:
            st.write('You manage to slip into the VIP area, but find nothing of immediate interest. Marcelline is speaking to someone, but their conversation is too hushed to discern anything useful.')

        if st.session_state.romance == 'Alex':
            st.session_state.relationship_scores['Alex'] += (1 * relationship_gain_multiplier)
            st.write('Alex spots you, their eyes widening. They give a quick, almost imperceptible nod of approval, a silent acknowledgment of your daring.')
    elif choice == 'observe_marcelline_alex':
        st.session_state.player_observant += 1 # Increase observant stat
        st.write('You watch Marcelline and Alex. Alex seems uneasy, fidgeting as Marcelline speaks with intense gravity. Alex keeps glancing your way, as if torn. You realize their relationship is more complex than it seems.')
        if st.session_state.romance == 'Alex':
            st.session_state.relationship_scores['Alex'] -= (1 * relationship_gain_multiplier) # Can slightly decrease if you just observe, showing less direct action
            st.write('Alex catches your eye and gives a subtle, almost imperceptible shake of their head, as if warning you away, but also a hint of disappointment in your inaction.')
    elif choice == 'find_east_wing_clue':
        st.write('Guided by your clues, you discreetly investigate a section of the wall behind a large tapestry. With a soft click, a hidden door slides open, revealing a dusty, narrow **Secret Passage** leading down into darkness.')
        st.write('You have found the way to the East Wing. What do you do inside?')
        # Direct transition to the new 'hidden_study' scene.
        st.button('Proceed into the Hidden Study.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'enter_study'}))
        show_general_secret_passage_options = False # Do NOT show general options here, as player is entering new scene
    elif choice == 'press_blake':
        st.session_state.relationship_scores['Blake'] += (1 * relationship_gain_multiplier)
        # Skill check for Blake to reveal information, influenced by social grace and difficulty.
        if random.randint(1,5) <= (skill_check_threshold + st.session_state.social_grace):
            st.write('You find Blake looking incredibly nervous. "Okay, okay! She keeps a ledger... in her private study, in the East Wing. It details everything: the sabotages, the blackmail, the disappearances of former contestants!" Blake is visibly terrified. "Please, just get me out of here."')
            if '📓 Marcelline\'s Ledger' not in st.session_state.inventory:
                st.session_state.inventory.append('📓 Marcelline\'s Ledger')
                st.session_state.clues_collected.append('Marcelline\'s Ledger (Evidence of crimes)')
            st.write('You now know about **📓 Marcelline\'s Ledger** and where to find it.')
        else:
            st.write('You try to press Blake, but they clam up, clearly too afraid to reveal more. "I\'ve said too much already!" they whisper, hurrying away.')
    elif choice == 'examine_chess_piece':
        st.write('You examine the chess piece more closely. It\'s a knight, carved from dark wood, with a small, almost invisible inscription on its base: "The game is played in the shadows." This doesn\'t give you a direct clue, but it adds to the mansion\'s ominous atmosphere, hinting at a larger conspiracy.')
        st.session_state.player_observant += 1 # Boost observant for attention to detail
        if 'examined_chess_piece' not in st.session_state.clues_collected:
            st.session_state.clues_collected.append('examined_chess_piece') # Mark as examined
        st.write("\n---")
        st.write('What do you do next in the mansion\'s hidden passages?')
        # These buttons lead back to secret_passage scene with new choices.
        st.button('Sneak into the VIP Area, where Marcelline is heading.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'sneak_vip'}))
        st.button('Observe Marcelline and Alex closely from a distance.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'observe_marcelline_alex'}))
        if any(clue in st.session_state.inventory for clue in ['🗺️ Jordan\'s Map', '🗝️ Tarnished Key', '📜 Faded Invitation', '📜 Cryptic Note']):
            st.button('Attempt to find the East Wing entrance based on your clues.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'find_east_wing_clue'}))
        if '📝 Blake\'s Confession' in st.session_state.inventory:
            st.button('Try to talk to Blake again, press for more information.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'press_blake'}))
        show_general_secret_passage_options = False # Do NOT show the general options after this specific interaction
    elif choice == 'examine_bracelet':
        st.write('You examine Jennifer\'s broken bracelet. It\'s intricate, with a small, almost invisible clasp. You notice a tiny, almost hidden etching on the inside: a stylized ' + '\u2622' + ' (alchemical symbol for sulfur/fire) and the initials "M.V." This might be a symbol or initials related to Marcelline or her family.')
        st.session_state.player_observant += 1
        if 'examined_bracelet' not in st.session_state.clues_collected:
            st.session_state.clues_collected.append('examined_bracelet')
        if 'M.V. Initials Clue' not in st.session_state.clues_collected:
            st.session_state.clues_collected.append('M.V. Initials Clue') # New clue
            if '💎 Vintage Locket Fragment' not in st.session_state.inventory:
                st.session_state.inventory.append('💎 Vintage Locket Fragment') # New item
                st.write('As you turn it over, a tiny fragment of a **💎 Vintage Locket Fragment** falls out of the clasp, bearing the same "M.V." etching.')

        st.write("\n---")
        st.write('What do you do next in the mansion\'s hidden passages?')
        # These buttons lead back to secret_passage scene with new choices.
        st.button('Sneak into the VIP Area, where Marcelline is heading.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'sneak_vip'}))
        st.button('Observe Marcelline and Alex closely from a distance.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'observe_marcelline_alex'}))
        if any(clue in st.session_state.inventory for clue in ['🗺️ Jordan\'s Map', '🗝️ Tarnished Key', '📜 Faded Invitation', '📜 Cryptic Note']):
            st.button('Attempt to find the East Wing entrance based on your clues.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'find_east_wing_clue'}))
        if '📝 Blake\'s Confession' in st.session_state.inventory:
            st.button('Try to talk to Blake again, press for more information.', on_click=lambda: st.query_params.update({'scene': 'secret_passage', 'choice': 'press_blake'}))
        show_general_secret_passage_options = False

    else: # This block runs when the scene is first entered without a specific 'choice' or if a non-branching choice was made.
        st.write('You\'ve found a way into a hidden part of the mansion—a wing filled with Marcelline’s darkest secrets. The air is heavy with dust and whispers of past schemes. Evidence of Marcelline’s dark deeds surrounds you. What do you prioritize?')
        # Ensure that if the player was already in East Wing via 'find_east_wing_clue', they go to hidden_study.
        if choice == 'find_east_wing_clue':
            st.button('Proceed into the Hidden Study.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'enter_study'}))
            show_general_secret_passage_options = False
        else:
            show_general_secret_passage_options = True

    # Only show these buttons if the flag allows it (i.e., not after specific direct navigation).
    if show_general_secret_passage_options:
        # These are options that lead to the 'hidden_study' scene.
        st.button('Enter the hidden study for a thorough search.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'general_search_study'}))


# NEW SCENE: The Hidden Study (formerly secret_passage_details)
elif scene == 'hidden_study':
    st.session_state.story_progress = 85 # Increased progress
    st.write('You find yourself in a dimly lit, dusty study, heavy with the scent of old paper and stale perfume. Bookshelves line the walls, filled with ominous-looking tomes. A large, ornate desk dominates the center of the room. This is clearly where Marcelline conducts her more clandestine affairs.')

    # Display options for searching the study.
    st.write('What do you focus on?')
    if '📓 Marcelline\'s Ledger' not in st.session_state.inventory:
        st.button('Search the desk for Marcelline\'s Ledger.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'find_ledger'}))
    if '📜 Ancient Document' not in st.session_state.inventory:
        st.button('Examine the bookshelves for unusual documents.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'examine_document'}))
    if '✉️ Coded Letter' not in st.session_state.inventory and 'Coded Letter (Benefactor)' not in st.session_state.clues_collected:
        st.button('Look for hidden compartments or unusual objects.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'decipher_letter_search'}))
    if '📸 Hidden Camera' not in st.session_state.inventory:
        st.button('Inspect the room for surveillance devices.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'find_hidden_camera'}))
    if '💎 Vintage Locket Fragment' in st.session_state.inventory and 'Vintage Locket (Complete)' not in st.session_state.inventory:
        st.button('Search for the other half of the Vintage Locket.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'find_locket_half'}))
    if '📜 Cryptic Note' in st.session_state.inventory and 'Deciphered Cryptic Note' not in st.session_state.clues_collected:
        st.button('Try to decipher the Cryptic Note fully.', on_click=lambda: st.query_params.update({'scene': 'hidden_study', 'choice': 'decipher_cryptic_note'}))

    # After any action in hidden_study, offer option to leave or proceed to next major scene.
    st.write("\n---")
    st.write('You\'ve explored this hidden study. It\'s time to face the consequences of your discoveries.')
    st.button('Return to the Midnight Ball to plan your final move.', on_click=lambda: st.query_params.update({'scene': 'marcelline_trap', 'choice': 'leave_study_ready'}))

    # Outcomes of specific searches within the hidden study.
    if choice == 'find_ledger':
        if '📓 Marcelline\'s Ledger' not in st.session_state.inventory:
            st.session_state.inventory.append('📓 Marcelline\'s Ledger')
            st.session_state.clues_collected.append('Marcelline\'s Ledger (Detailed Crimes)')
        st.write('You quickly locate **📓 Marcelline\'s Ledger**. It\'s a chilling account of manipulation, sabotage, and even implied disappearances of past contestants who got too close to the truth. Blake\'s words ring true. This is powerful evidence.')
    elif choice == 'examine_document':
        if '📜 Ancient Document' not in st.session_state.inventory:
            st.session_state.inventory.append('📜 Ancient Document')
            st.session_state.clues_collected.append('Ancient Document (Patron\'s Bloodline)')
        st.write('The **📜 Ancient Document** reveals Marcelline\'s family has a long history of gaining power and wealth through ruthless means, often eliminating rivals or those who stand in their way. It speaks of a "Patron\'s Bloodline" and a pact. This ties into a larger conspiracy.')
    elif choice == 'decipher_letter_search':
        if '✉️ Coded Letter' not in st.session_state.inventory:
            # Chance to find the letter if not found already, influenced by observant stat and difficulty.
            if random.randint(1,5) <= (skill_check_threshold + st.session_state.player_observant):
                st.session_state.inventory.append('✉️ Coded Letter')
                st.session_state.clues_collected.append('Coded Letter (Benefactor\'s Plot)')
                st.write('You discover a cleverly concealed drawer containing a **✉️ Coded Letter**. After some effort, you decipher it. It\'s a communication from an unknown "Benefactor," discussing a "final phase" and the "elimination of loose ends." The Benefactor seems to be Marcelline\'s true mastermind. This is a critical piece of the puzzle.')
            else:
                st.write('You search diligently for hidden compartments, but find nothing unusual.')
        else:
            st.write('You already have the coded letter, no new one is found here.')
    elif choice == 'find_hidden_camera':
        if '📸 Hidden Camera' not in st.session_state.inventory:
            # Chance to find hidden camera, influenced by observant stat and difficulty.
            if random.randint(1,5) <= (skill_check_threshold + st.session_state.player_observant):
                st.session_state.inventory.append('📸 Hidden Camera')
                st.session_state.clues_collected.append('Hidden Camera (Mansion surveillance)')
                st.write('Your heightened awareness pays off! You discover a **📸 Hidden Camera** disguised as a smoke detector. It\'s clear Marcelline has been monitoring everything. You take it as evidence.')
            else:
                st.write('You search for surveillance devices, but they are too well-hidden. You find nothing.')
        else:
            st.write('You\'ve already found a hidden camera.')
    elif choice == 'find_locket_half': # New item discovery
        if '💎 Vintage Locket (Complete)' not in st.session_state.inventory:
            if '💎 Vintage Locket Fragment' in st.session_state.inventory:
                # Skill check to find the other half, influenced by observant stat and difficulty.
                if random.randint(1,5) <= (skill_check_threshold + st.session_state.player_observant):
                    st.session_state.inventory.remove('💎 Vintage Locket Fragment')
                    st.session_state.inventory.append('💎 Vintage Locket (Complete)')
                    st.session_state.clues_collected.append('Vintage Locket (Complete)')
                    st.write('You meticulously search, and tucked inside a false bottom of a drawer, you find the other half of the locket! It fits perfectly with your fragment. The **💎 Vintage Locket (Complete)** opens to reveal a faded miniature portrait of a woman who strikingly resembles Marcelline, but with a kinder expression. On the back, an inscription reads: "To my beloved, M.V. - Always Remember the Pact."')
                    if 'M.V. Initials Clue' not in st.session_state.clues_collected:
                        st.session_state.clues_collected.append('M.V. Initials Clue')
                else:
                    st.write('You search for the locket\'s other half, but it remains elusive in this complex room.')
            else:
                st.write('You don\'t have a locket fragment to complete.')
        else:
            st.write('You\'ve already completed the Vintage Locket.')
    elif choice == 'decipher_cryptic_note': # New item use
        if '📜 Cryptic Note' in st.session_state.inventory and 'Deciphered Cryptic Note' not in st.session_state.clues_collected:
            # Skill check to decipher the note, influenced by observant stat and difficulty.
            if random.randint(1,5) <= (skill_check_threshold + st.session_state.player_observant):
                st.session_state.clues_collected.append('Deciphered Cryptic Note')
                st.write('You spend time carefully analyzing the **📜 Cryptic Note**. You realize it\'s a coded message from a former victim, outlining a dead drop location in the mansion\'s garden for incriminating evidence against Marcelline, intended for an "investigator." The date on it is recent. This could be a new source of evidence!')
                if '🗺️ Garden Dead Drop Location' not in st.session_state.inventory:
                    st.session_state.inventory.append('🗺️ Garden Dead Drop Location')
                    st.session_state.clues_collected.append('Garden Dead Drop Location')
            else:
                st.write('You try to decipher the cryptic note, but its code proves too complex for now.')
        else:
            st.write('You do not have a cryptic note to decipher, or you\'ve already deciphered it.')

# NEW SCENE: Marcelline's Trap
elif scene == 'marcelline_trap':
    st.session_state.story_progress = 90
    st.write('As you prepare to make your move, a suave assistant approaches you with an urgent message: "Marcelline requests your presence in her private lounge. She wishes to discuss your exceptional talent... and perhaps offer you a unique opportunity."')
    st.write('You sense this could be a trap, but also an opportunity for a final confrontation.')

    # If player just came from the study, acknowledge it.
    if choice in ['leave_study_early', 'leave_study_full', 'leave_study_ready']:
        st.write('You left the hidden study and are now back in the main ball, facing this new challenge.')

    st.write("\n**What do you do?**")
    # Choices for how to handle Marcelline's invitation.
    st.button('Accept the invitation, playing along to see her hand.', on_click=lambda: st.query_params.update({'scene': 'marcelline_trap', 'choice': 'accept_invitation'}))
    st.button('Decline the invitation, choosing to act on your own terms.', on_click=lambda: st.query_params.update({'scene': 'confrontation', 'choice': 'avoid_trap_direct_confront'}))

    if choice == 'accept_invitation':
        st.write('\n---')
        st.write('You enter Marcelline\'s opulent private lounge. She smiles, a predatory gleam in her eyes. "My dear, I\'ve been watching you. You have a unique talent. Join me. Become my protégé, and together we can control this entire industry. All you have to do is forget what you\'ve seen and pledge your loyalty."')
        st.write('You notice a shimmering antique brooch on her lapel that catches your eye. It looks oddly familiar.')
        # Check for the complete vintage locket and its connection to Marcelline's brooch.
        if '💎 Vintage Locket (Complete)' in st.session_state.inventory:
            st.write('The brooch on her lapel is the other half of your **💎 Vintage Locket (Complete)**! The image inside your locket matches a distinct detail on her brooch. She recognizes the locket in your possession, and her smile falters for a fraction of a second. This is the "M.V." you\'ve been searching for.')
            st.session_state.player_observant += 1 # Boost for noticing this
            if 'Marcelline\'s Locket/Brooch Connection' not in st.session_state.clues_collected:
                st.session_state.clues_collected.append('Marcelline\'s Locket/Brooch Connection') # New clue
        else:
            st.write('The brooch looks expensive, but you don\'t recognize any specific significance to it.')

        st.write('\n**How do you respond to Marcelline\'s offer?**')
        # Choices for responding to Marcelline's trap/offer.
        st.button('Accept her offer, pretending loyalty to gather more intel.', on_click=lambda: st.query_params.update({'scene': 'confrontation', 'choice': 'feign_loyalty'}))
        st.button('Bluff, hinting you have evidence without revealing it.', on_click=lambda: st.query_params.update({'scene': 'confrontation', 'choice': 'bluff_evidence'}))
        st.button('Flatly refuse and prepare for a direct confrontation.', on_click=lambda: st.query_params.update({'scene': 'confrontation', 'choice': 'refuse_direct_confront'}))

# Scene: Confrontation (Final Showdown)
elif scene == 'confrontation':
    st.session_state.story_progress = 100
    st.write('The final show unfolds, the grand ballroom transformed into a dazzling runway. Marcelline stands at the podium, a triumphant smile on her face. This is your last chance to act.')

    # Count the number of significant evidence pieces collected.
    required_evidence_for_full_win = 0
    if '📓 Marcelline\'s Ledger' in st.session_state.inventory: required_evidence_for_full_win += 1
    if '📜 Ancient Document' in st.session_state.inventory: required_evidence_for_full_win += 1
    if '✉️ Coded Letter' in st.session_state.inventory: required_evidence_for_full_win += 1
    if '📸 Hidden Camera' in st.session_state.inventory: required_evidence_for_full_win += 1
    if '📱 Suspicious Photo' in st.session_state.inventory: required_evidence_for_full_win += 1
    if '💎 Vintage Locket (Complete)' in st.session_state.inventory: required_evidence_for_full_win += 1
    if 'Deciphered Cryptic Note' in st.session_state.clues_collected: required_evidence_for_full_win += 1 # Note itself is the evidence

    # Check if Blake and Maya will support the player.
    blake_supports_you = '📝 Blake\'s Confession' in st.session_state.inventory and st.session_state.relationship_scores['Blake'] > 0
    maya_supports_you = '📜 Maya\'s Observation' in st.session_state.inventory and st.session_state.relationship_scores['Maya'] > 0

    # Handle the choices made in the 'marcelline_trap' scene.
    if choice == 'avoid_trap_direct_confront':
        st.write('You wisely avoided Marcelline\'s private meeting, knowing it was a trap. You are now ready for a direct confrontation on your terms.')
        choice = 'public_confrontation' # Force this path for the final logic.

    elif choice == 'feign_loyalty':
        st.write('You faked your loyalty, giving Marcelline a false sense of security. Now, with the show commencing, you reveal your true intentions.')
        # Skill check for extra impact from feigning loyalty.
        if random.randint(1,5) <= (skill_check_threshold + st.session_state.social_grace):
            st.write('Your feigned loyalty successfully caught her off guard, giving you a powerful edge!')
            required_evidence_for_full_win += 1 # Slight bonus for cunning
        else:
            st.write('Marcelline looks momentarily surprised, but quickly regains her composure. She\'s not easily fooled.')
        choice = 'public_confrontation' # Force this path.

    elif choice == 'bluff_evidence':
        st.write('You hinted at evidence, trying to intimidate Marcelline. Her eyes narrow. She knows you\'re holding something, but perhaps not everything.')
        # Skill check for convincing bluff, influenced by observant stat.
        if st.session_state.player_observant >= skill_check_threshold:
            st.write('Your bluff is convincing, and Marcelline looks genuinely unnerved. She\'s on the defensive.')
            required_evidence_for_full_win += 0.5 # Small bonus
        else:
            st.write('Marcelline scoffs. "A bluff, darling? You\'ll need more than that." She seems unimpressed.')
        choice = 'public_confrontation' # Force this path.

    elif choice == 'refuse_direct_confront':
        st.write('You flatly refused Marcelline\'s offer, making it clear you are her adversary. The tension in the room escalates.')
        choice = 'public_confrontation' # Force this path.

    # --- Public Confrontation Ending Logic ---
    if choice == 'public_confrontation':
        st.write('\n---')
        st.write('You step forward, microphone in hand, and prepare to expose Marcelline to the assembled press and fashion elite.')

        # Calculate win score for public confrontation.
        win_score = 0
        if st.session_state.fashion_score == 'High': win_score += 1
        if required_evidence_for_full_win >= 3: win_score += 1 # Need at least 3 strong pieces of evidence
        if blake_supports_you: win_score += 1
        if maya_supports_you: win_score += 1 # Maya's support contributes to public win

        if win_score >= 3: # Higher threshold for a public win
            st.write('🎉 **VICTORY!** Your stunning design captivates the audience, giving you the platform you need. With compelling evidence, you expose Marcelline\'s crimes and machinations. The fashion world is shaken. Your love interest publicly supports you, solidifying your bond and a future together.')
            st.balloons() # Add confetti for a public victory!
            if blake_supports_you:
                st.write('Blake, though trembling, steps forward to corroborate your claims, adding undeniable weight to your accusation!')
            if maya_supports_you:
                st.write('Maya, emboldened by your bravery, also steps forward, confirming Marcelline\'s manipulative tactics and bolstering your case!')

            # Romance-specific triumphant dialogue for maxed relationships.
            if st.session_state.romance == 'Alex':
                if st.session_state.relationship_scores['Alex'] >= (4 * relationship_gain_multiplier) and st.session_state.date_opportunity_taken:
                    st.write('Alex sweeps you into a passionate embrace, their eyes shining with fierce admiration. "My star," they whisper, "You truly are the greatest show. Our future together... it\'s going to be legendary."')
                else:
                    st.write('Alex steps forward, a confident smile on their face. "This designer is not just talented, but truly fearless. I\'m proud to stand by them." They take your hand, their touch sending a thrill through you.')
                st.session_state.relationship_scores['Alex'] = 5
            elif st.session_state.romance == 'Jordan':
                if st.session_state.relationship_scores['Jordan'] >= (4 * relationship_gain_multiplier) and st.session_state.date_opportunity_taken:
                    st.write('Jordan, looking less nervous than ever, addresses the crowd, their voice clear and strong. "Their integrity is as profound as their art. The truth they\'ve revealed... it will change everything. And I will be by their side through it all." They reach for your hand, a quiet promise in their gaze.')
                else:
                    st.write('Jordan, looking less nervous than ever, addresses the crowd. "Their integrity is as profound as their art. The truth they\'ve revealed... it will change everything." They offer you a genuine, heartfelt smile.')
                st.session_state.relationship_scores['Jordan'] = 5
            elif st.session_state.romance == 'Taylor':
                if st.session_state.relationship_scores['Taylor'] >= (4 * relationship_gain_multiplier) and st.session_state.date_opportunity_taken and st.session_state.final_romance_dialogue_unlocked:
                    st.write('Taylor appears by your side, his demeanor calm but his eyes ablaze with emotion. "The truth always finds a way," he states, his gaze never leaving yours. "And you, my dear, are the truth I\'ve waited for. Our future, together, will be far more fulfilling than any competition." He gently cups your face, a tender kiss sealing your triumph.')
                else:
                    st.write('Taylor appears by your side, his demeanor calm but firm. "The truth always finds a way," he states, his gaze reassuring. "And this is just the beginning for a talent such as yours." He gives you a subtle, encouraging squeeze of the hand.')
                st.session_state.relationship_scores['Taylor'] = 5
            st.write('Marcelline is apprehended, but as she\'s led away, she gives you a chilling smile. "You\'ve only scratched the surface. The Benefactor will not be pleased."')
        elif win_score >= 1: # Partial success condition for public confrontation.
            st.write('❌ **PARTIAL SUCCESS, BUT RISKY.** Your design is a hit, and you make a powerful accusation. Without enough concrete evidence or widespread support, Marcelline manages to sow doubt. The crowd is divided. You\'ve damaged her reputation, but she retains some influence. Your love interest might be impressed by your bravery, but the future is uncertain.')
            if blake_supports_you:
                 st.write('Blake starts to speak, but Marcelline quickly silences them, making their testimony seem like a desperate lie.')
            if maya_supports_you:
                st.write('Maya speaks up, but her voice is drowned out by the chaos, and Marcelline dismisses her as a jealous rival.')
            if st.session_state.romance == 'Alex':
                st.write('Alex looks torn. "That was bold," they say, "but perhaps a bit too soon." Their support feels hesitant.')
            elif st.session_state.romance == 'Jordan':
                st.write('Jordan nods, "You tried. The truth will come out, eventually." They still believe in you, but the romantic tension lessens.')
            elif st.session_state.romance == 'Taylor':
                st.write('Taylor sighs. "A valiant effort, but not enough. We must be more patient." The bond holds, but the success is bittersweet.')
        else: # Failed public exposure.
            st.write('💥 **FAILED EXPOSURE.** Your accusations, while bold, lack the weight of irrefutable proof or sufficient support. Marcelline easily dismisses you, painting you as a disgruntled rival. You are publicly humiliated, and Marcelline\'s schemes continue unchecked. Your love interest distances themselves, seeing you as a liability.')
            if st.session_state.romance:
                st.session_state.relationship_scores[st.session_state.romance] = 0
                st.write(f'Your love interest, {st.session_state.romance}, seems to fade into the background, perhaps regretting their association with your failed attempt.')
            if blake_supports_you:
                st.write('Blake shakes their head, disappearing into the crowd, clearly unwilling to risk themselves further.')
            if maya_supports_you:
                st.write('Maya looks at you with pity, unable to offer any help now.')

    # --- Share with Taylor Ending Logic ---
    elif choice == 'share_with_taylor':
        st.write('\n---')
        st.write('You quietly present your compiled evidence to Taylor, trusting his discretion.')
        
        # Count significant evidence for Taylor's path.
        significant_evidence_count = 0
        if '📓 Marcelline\'s Ledger' in st.session_state.inventory: significant_evidence_count += 1
        if '📜 Ancient Document' in st.session_state.inventory: significant_evidence_count += 1
        if '✉️ Coded Letter' in st.session_state.inventory: significant_evidence_count += 1
        if '📸 Hidden Camera' in st.session_state.inventory: significant_evidence_count += 1
        if '💎 Vintage Locket (Complete)' in st.session_state.inventory: significant_evidence_count += 1
        if 'Deciphered Cryptic Note' in st.session_state.clues_collected: significant_evidence_count += 1

        if significant_evidence_count >= 3: # Adjusted for more clues
            st.write('🤝 **QUIET JUSTICE.** Taylor, with your strong evidence, meticulously works behind the scenes. Marcelline is discreetly apprehended by authorities she couldn\'t bribe or manipulate. You may not win the competition, but you save countless others from her schemes. Your bond with Taylor deepens, and you find true love and a partner in justice.')
            st.balloons() # Add confetti for a discreet victory!
            if st.session_state.romance == 'Taylor':
                if st.session_state.relationship_scores['Taylor'] >= (4 * relationship_gain_multiplier) and st.session_state.date_opportunity_taken and st.session_state.final_romance_dialogue_unlocked:
                    st.write('Taylor looks at you, his eyes filled with profound gratitude and a tender, genuine smile. He takes your hand, his touch warm and comforting. "We did it. And my dearest, this is just the beginning of our story. My loyalty to justice is unwavering, but my devotion to you... it transcends all."')
                else:
                    st.write('Taylor looks at you, his eyes filled with gratitude and a rare, tender smile. He takes your hand, his touch warm and comforting. "We did it. Thank you for trusting me. Our future, together, will be far more fulfilling than any competition."')
                st.session_state.relationship_scores['Taylor'] = 5
            elif st.session_state.romance:
                st.write(f'Your chosen love interest, {st.session_state.romance}, finds out about your quiet efforts. While initially surprised, they admire your integrity and strength. They choose to join you in a quieter life away from the spotlight, supporting your newfound purpose, truly seeing you for who you are.')
                st.session_state.relationship_scores[st.session_state.romance] = 4
            else:
                 st.write('You feel a strong connection to Taylor, a quiet understanding that goes beyond words. You may not have found a grand romance, but you\'ve found a powerful ally and friend.')
            if '📝 Blake\'s Confession' in st.session_state.inventory:
                 st.write('Days later, you hear that Blake has been released from any obligations to Marcelline. They contact you, grateful, and promise to help you in any way they can in the future.')
                 st.session_state.relationship_scores['Blake'] = 5
            if '📜 Maya\'s Observation' in st.session_state.inventory:
                st.write('Maya is relieved and grateful, knowing Marcelline can no longer threaten her. She becomes a steadfast friend.')
                st.session_state.relationship_scores['Maya'] = 5
        else: # Insufficient evidence for Taylor's path.
            st.write('😞 **INSUFFICIENT EVIDENCE.** Taylor appreciates your trust, but the evidence you provide is too flimsy to bring down someone as powerful and connected as Marcelline. He promises to keep trying, but for now, the truth remains buried. You lose the competition, and the situation remains unresolved.')
            if st.session_state.romance:
                st.write(f'Your love interest, {st.session_state.romance}, is disappointed by the lack of progress and the unresolved mystery. Your relationship strains under the weight of Marcelline\'s continued power.')
            if '📝 Blake\'s Confession' in st.session_state.inventory:
                st.write('Blake remains under Marcelline\'s thumb, their confession unable to be used without more leverage.')
            if '📜 Maya\'s Observation' in st.session_state.inventory:
                st.write('Maya is still under threat, and expresses her disappointment that Marcelline remains free.')

    # --- Stay Silent Ending Logic ---
    elif choice == 'stay_silent_confront':
        st.write('\n---')
        st.write('You choose to stay silent. The show proceeds without incident. Marcelline wins, her smile radiating false triumph. The truth remains buried, and the dark underbelly of the fashion world continues its operations.')
        if st.session_state.romance:
            st.write(f'Your chosen love interest, {st.session_state.romance}, expresses disappointment in your inaction, or perhaps, relief at avoiding danger. Your relationship is strained, but you are safe, for now.')
        else:
            st.write('You return to your normal life, forever haunted by the secrets you uncovered but chose not to reveal.')
        if '📝 Blake\'s Confession' in st.session_state.inventory:
            st.write('Blake looks at you with a mixture of fear and betrayal, knowing you chose not to act on their confession. They are still bound by Marcelline\'s threats.')
            st.session_state.relationship_scores['Blake'] = 0
        if '📜 Maya\'s Observation' in st.session_state.inventory:
            st.write('Maya avoids your gaze, clearly feeling let down and still vulnerable to Marcelline\'s schemes.')
            st.session_state.relationship_scores['Maya'] = 0


    # --- Game Summary ---
    st.write("\n---")
    st.subheader("Your Fashion Fatal Journey Summary")
    st.write(f"**Fashion Score:** {st.session_state.fashion_score}")
    st.write(f"**Observant Stat:** {st.session_state.player_observant}")
    st.write(f"**Social Grace Stat:** {st.session_state.social_grace}")
    st.write(f"**Difficulty Played On:** {st.session_state.difficulty}")

    st.write(f"**Inventory:** {', '.join(st.session_state.inventory) if st.session_state.inventory else 'None'}")
    st.write(f"**Romantic Interest:** {st.session_state.romance if st.session_state.romance else 'None'}")
    st.write(f"**Final Relationship Scores:** {st.session_state.relationship_scores}")
    st.write(f"**Clues Collected:** {', '.join(st.session_state.clues_collected) if st.session_state.clues_collected else 'None'}")

    # Restart Game button clears session state and resets to the beginning.
    st.button('Restart Game', on_click=lambda: [st.session_state.clear(), st.query_params.update({'scene': 'arrival', 'choice': None})])

