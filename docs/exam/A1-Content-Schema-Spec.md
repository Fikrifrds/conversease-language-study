# A1 Real Exam - Content Schema Specification

## 1. Overview

**Level**: A1 (Beginner)  
**Duration**: 45 minutes  
**Total Items**: 35-42 items  
**Sections**: 5 (Listening, Reading, Grammar & Vocabulary, Speaking, Writing)

## 2. File Structure

```
content/curriculum/english/A1/exam/
├── blueprint.yaml              # Exam configuration
├── audio_manifest.yaml         # Listening audio assets
├── answer_key.yaml             # Correct answers for objective items
├── rubric.yaml                 # Scoring rubrics for subjective items
└── items/
    ├── listening.yaml          # 8-10 items
    ├── reading.yaml            # 5-7 items
    ├── grammar_vocabulary.yaml # 10-12 items
    ├── speaking.yaml           # 3-4 tasks
    └── writing.yaml            # 1-2 tasks
```

## 3. Blueprint Schema

```yaml
# blueprint.yaml
exam:
  level_code: A1
  version: "1.0.0"
  title: "A1 English Proficiency Exam"
  description: "Assessment of basic English communication skills"
  
  config:
    total_duration_minutes: 45
    allow_pause: true
    max_attempts: 3
    cooldown_days: 30
    passing_threshold: 60
    section_sequence: strict
  
  sections:
    - id: listening
      type: listening
      title: "Listening"
      description: "Understand simple conversations and instructions"
      sequence_order: 1
      weight: 25
      minimum_score: 50
      duration_minutes: 10
      
    - id: reading
      type: reading
      title: "Reading"
      description: "Understand simple texts and signs"
      sequence_order: 2
      weight: 20
      minimum_score: 50
      duration_minutes: 8
      
    - id: grammar_vocabulary
      type: grammar_vocabulary
      title: "Grammar & Vocabulary"
      description: "Use basic grammar and common words"
      sequence_order: 3
      weight: 20
      minimum_score: 50
      duration_minutes: 10
      
    - id: speaking
      type: speaking
      title: "Speaking"
      description: "Introduce yourself and ask simple questions"
      sequence_order: 4
      weight: 25
      minimum_score: 50
      duration_minutes: 5
      
    - id: writing
      type: writing
      title: "Writing"
      description: "Write simple sentences and fill in forms"
      sequence_order: 5
      weight: 10
      minimum_score: 40
      duration_minutes: 2
```

## 4. Item Schema

### 4.1 Listening Items

```yaml
# items/listening.yaml
section_id: listening
items:
  - id: L1
    type: mcq
    difficulty: easy
    points: 1
    skills: [listening_comprehension, gist]
    
    stimulus:
      type: audio
      content_ref: listening_audio_001
      audio_url: /audio/a1/exam/listening_001.mp3
      duration_seconds: 15
      play_count_limit: 2
    
    prompt: "What is the main topic of the conversation?"
    
    choices:
      - id: A
        text: "Ordering food"
        isCorrect: true
      - id: B
        text: "Buying clothes"
        isCorrect: false
      - id: C
        text: "Booking a hotel"
        isCorrect: false
      - id: D
        text: "Asking for directions"
        isCorrect: false

  - id: L2
    type: fill_in_blank
    difficulty: medium
    points: 1
    skills: [listening_comprehension, detail]
    
    stimulus:
      type: audio
      content_ref: listening_audio_002
      audio_url: /audio/a1/exam/listening_002.mp3
      duration_seconds: 20
      play_count_limit: 2
    
    prompt: "Listen and complete the sentence."
    
    question_text: "The train leaves at _____ o'clock."
    correct_answer: "9"
    acceptable_answers: ["9", "nine", "9:00", "nine o'clock"]

  - id: L3
    type: matching
    difficulty: medium
    points: 2
    skills: [listening_comprehension, detail]
    
    stimulus:
      type: audio
      content_ref: listening_audio_003
      audio_url: /audio/a1/exam/listening_003.mp3
      duration_seconds: 45
      play_count_limit: 2
    
    prompt: "Match each person with what they want to order."
    
    left_items:
      - id: P1
        text: "Maria"
      - id: P2
        text: "John"
      - id: P3
        text: "Lisa"
    
    right_items:
      - id: F1
        text: "Coffee"
      - id: F2
        text: "Tea"
      - id: F3
        text: "Orange juice"
    
    correct_matches:
      P1: F2  # Maria - Tea
      P2: F3  # John - Orange juice
      P3: F1  # Lisa - Coffee
```

### 4.2 Reading Items

```yaml
# items/reading.yaml
section_id: reading
items:
  - id: R1
    type: mcq
    difficulty: easy
    points: 1
    skills: [reading_comprehension, gist]
    
    stimulus:
      type: text
      content: |
        CAFÉ CENTRAL
        
        Opening hours:
        Monday - Friday: 7:00 - 20:00
        Saturday: 8:00 - 18:00
        Sunday: CLOSED
        
        Free Wi-Fi available!
    
    prompt: "When can you visit the café on Sunday?"
    
    choices:
      - id: A
        text: "At 9:00 AM"
        isCorrect: false
      - id: B
        text: "At 12:00 PM"
        isCorrect: false
      - id: C
        text: "The café is closed"
        isCorrect: true
      - id: D
        text: "At 7:00 PM"
        isCorrect: false

  - id: R2
    type: fill_in_blank
    difficulty: medium
    points: 1
    skills: [reading_comprehension, detail]
    
    stimulus:
      type: text
      content: |
        Hello! My name is Anna. I am 25 years old and I live in Berlin. 
        I work as a teacher at a language school. I teach English and Spanish. 
        In my free time, I like reading books and going for walks in the park.
    
    prompt: "Read the text and answer the question."
    
    question_text: "Anna works as a _____."
    correct_answer: "teacher"
    acceptable_answers: ["teacher", "a teacher"]

  - id: R3
    type: mcq
    difficulty: medium
    points: 1
    skills: [reading_comprehension, inference]
    
    stimulus:
      type: text
      content: |
        From: sarah@email.com
        To: mom@email.com
        Subject: Good news!
        
        Dear Mom,
        
        I have some great news! I got the job at the hospital! 
        I start next Monday. The salary is good and I get 
        25 days of vacation every year. I am so happy!
        
        Love,
        Sarah
    
    prompt: "What can we learn about Sarah's new job?"
    
    choices:
      - id: A
        text: "She will work at a school."
        isCorrect: false
      - id: B
        text: "She has 15 days of vacation."
        isCorrect: false
      - id: C
        text: "She starts work on Monday."
        isCorrect: true
      - id: D
        text: "The salary is low."
        isCorrect: false
```

### 4.3 Grammar & Vocabulary Items

```yaml
# items/grammar_vocabulary.yaml
section_id: grammar_vocabulary
items:
  - id: GV1
    type: mcq
    difficulty: easy
    points: 1
    skills: [grammar, present_simple]
    
    stimulus:
      type: text
      content: "Choose the correct answer."
    
    prompt: "She _____ to work every day at 8:00 AM."
    
    choices:
      - id: A
        text: "go"
        isCorrect: false
      - id: B
        text: "goes"
        isCorrect: true
      - id: C
        text: "going"
        isCorrect: false
      - id: D
        text: "is go"
        isCorrect: false

  - id: GV2
    type: fill_in_blank
    difficulty: medium
    points: 1
    skills: [vocabulary, collocations]
    
    stimulus:
      type: text
      content: "Complete the sentence with the correct word."
    
    prompt: "I need to _____ a reservation at the restaurant."
    
    correct_answer: "make"
    acceptable_answers: ["make"]

  - id: GV3
    type: matching
    difficulty: easy
    points: 2
    skills: [vocabulary, everyday_objects]
    
    stimulus:
      type: text
      content: "Match the words with their descriptions."
    
    prompt: "Match each object with its description."
    
    left_items:
      - id: O1
        text: "Umbrella"
      - id: O2
        text: "Wallet"
      - id: O3
        text: "Backpack"
    
    right_items:
      - id: D1
        text: "Keeps you dry in the rain"
      - id: D2
        text: "Holds your money and cards"
      - id: D3
        text: "You wear it on your back to carry things"
    
    correct_matches:
      O1: D1
      O2: D2
      O3: D3

  - id: GV4
    type: mcq
    difficulty: medium
    points: 1
    skills: [grammar, prepositions]
    
    stimulus:
      type: text
      content: "Choose the correct preposition."
    
    prompt: "The meeting is _____ Monday morning _____ 9:00 AM."
    
    choices:
      - id: A
        text: "on / at"
        isCorrect: true
      - id: B
        text: "in / at"
        isCorrect: false
      - id: C
        text: "on / in"
        isCorrect: false
      - id: D
        text: "at / on"
        isCorrect: false
```

### 4.4 Speaking Tasks

```yaml
# items/speaking.yaml
section_id: speaking
items:
  - id: S1
    type: audio_response
    task_type: read_aloud
    difficulty: easy
    points: 5
    skills: [pronunciation, fluency]
    duration_seconds: 60
    
    stimulus:
      type: text
      content: "Hello. My name is Anna. I am from Italy. I live in Rome. I work in a hospital. I am a nurse. I like my job."
    
    prompt: "Read the text aloud. You have 60 seconds."
    
    rubric:
      criteria:
        - name: pronunciation
          weight: 40
          description: "Clear pronunciation of words"
        - name: fluency
          weight: 40
          description: "Natural flow and rhythm"
        - name: accuracy
          weight: 20
          description: "Reading the text correctly"

  - id: S2
    type: audio_response
    task_type: short_response
    difficulty: medium
    points: 10
    skills: [speaking, vocabulary, grammar]
    duration_seconds: 90
    
    stimulus:
      type: text
      content: "Tell me about your daily routine."
    
    prompt: "Describe your typical day. What time do you wake up? What do you do in the morning, afternoon, and evening? You have 90 seconds."
    
    rubric:
      criteria:
        - name: content
          weight: 30
          description: "Covers daily activities with time references"
        - name: vocabulary
          weight: 25
          description: "Uses appropriate everyday vocabulary"
        - name: grammar
          weight: 25
          description: "Uses present simple correctly"
        - name: fluency
          weight: 20
          description: "Speaks at a natural pace"

  - id: S3
    type: audio_response
    task_type: situational_response
    difficulty: medium
    points: 10
    skills: [speaking, functional_language, politeness]
    duration_seconds: 60
    
    stimulus:
      type: text
      content: "You are at a restaurant. The waiter brings you the wrong dish."
    
    prompt: "What would you say to the waiter? Be polite. You have 60 seconds."
    
    rubric:
      criteria:
        - name: appropriateness
          weight: 40
          description: "Uses polite language for the situation"
        - name: clarity
          weight: 30
          description: "Clearly explains the problem"
        - name: language
          weight: 30
          description: "Uses appropriate restaurant vocabulary"

  - id: S4
    type: audio_response
    task_type: extended_response
    difficulty: hard
    points: 15
    skills: [speaking, coherence, elaboration]
    duration_seconds: 120
    
    stimulus:
      type: text
      content: "Describe your favorite place in your city."
    
    prompt: "Talk about your favorite place. Where is it? Why do you like it? When do you go there? Who do you go with? You have 2 minutes."
    
    rubric:
      criteria:
        - name: content
          weight: 30
          description: "Provides detailed information about the place"
        - name: organization
          weight: 25
          description: "Presents ideas in a logical order"
        - name: vocabulary
          weight: 25
          description: "Uses descriptive vocabulary"
        - name: grammar
          weight: 20
          description: "Uses a variety of structures correctly"
```

### 4.5 Writing Tasks

```yaml
# items/writing.yaml
section_id: writing
items:
  - id: W1
    type: essay
    task_type: short_message
    difficulty: easy
    points: 5
    skills: [writing, functional_language, spelling]
    word_count:
      min: 20
      max: 40
      target: 30
    duration_minutes: 5
    
    stimulus:
      type: text
      content: "You are on vacation. Write a postcard to your friend."
    
    prompt: "Write a short postcard to your friend. Tell them:
      - Where you are
      - What the weather is like
      - What you are doing
      
      Write 20-40 words."
    
    rubric:
      criteria:
        - name: task_achievement
          weight: 30
          description: "Includes all three required points"
        - name: vocabulary
          weight: 25
          description: "Uses appropriate holiday vocabulary"
        - name: grammar
          weight: 25
          description: "Uses present continuous and present simple correctly"
        - name: spelling_punctuation
          weight: 20
          description: "Spells common words correctly, uses basic punctuation"

  - id: W2
    type: essay
    task_type: form_filling
    difficulty: medium
    points: 5
    skills: [writing, personal_information, capitalization]
    word_count:
      min: 10
      max: 20
      target: 15
    duration_minutes: 3
    
    stimulus:
      type: text
      content: "Complete the hotel registration form."
    
    prompt: "Fill in the form with your information:
      - First name: _____________
      - Last name: _____________
      - Country: _____________
      - Email: _____________"
    
    rubric:
      criteria:
        - name: completeness
          weight: 40
          description: "All four fields completed"
        - name: accuracy
          weight: 30
          description: "Appropriate personal information provided"
        - name: capitalization
          weight: 30
          description: "Proper names capitalized correctly"

  - id: W3
    type: essay
    task_type: guided_writing
    difficulty: hard
    points: 10
    skills: [writing, coherence, sentence_structure]
    word_count:
      min: 30
      max: 50
      target: 40
    duration_minutes: 7
    
    stimulus:
      type: text
      content: "Write about your best friend."
    
    prompt: "Write about your best friend. Include:
      - Their name and age
      - What they look like
      - What you do together
      - Why you like them
      
      Use the present simple. Write 30-50 words."
    
    rubric:
      criteria:
        - name: task_achievement
          weight: 30
          description: "Includes all four required points"
        - name: organization
          weight: 25
          description: "Ideas presented in logical order with linking words"
        - name: vocabulary
          weight: 25
          description: "Uses appropriate descriptive vocabulary"
        - name: grammar
          weight: 20
          description: "Uses present simple correctly for descriptions"
```

## 5. Audio Manifest

```yaml
# audio_manifest.yaml
exam_audio_assets:
  format: mp3
  sample_rate: 44100
  bit_rate: 128kbps
  
  assets:
    - id: listening_audio_001
      file: listening_001.mp3
      duration_seconds: 15
      transcript: |
        Waiter: Good afternoon. Can I take your order?
        Customer: Yes, please. I'd like a sandwich and a coffee.
        Waiter: Anything else?
        Customer: No, that's all. Thank you.
      
    - id: listening_audio_002
      file: listening_002.mp3
      duration_seconds: 20
      transcript: |
        Announcer: The next train to London will depart from platform 3 
        at 9:00 AM. Passengers are reminded to have their tickets ready 
        for inspection. Thank you.
      
    - id: listening_audio_003
      file: listening_003.mp3
      duration_seconds: 45
      transcript: |
        Waiter: Hello! Are you ready to order?
        Maria: Yes, I'd like a cup of tea, please.
        Waiter: And for you, sir?
        John: I'll have an orange juice.
        Waiter: Very good. And for the young lady?
        Lisa: Can I have a coffee, please?
        Waiter: Of course. I'll bring your drinks right away.
```

## 6. Answer Key

```yaml
# answer_key.yaml
objective_items:
  # Listening
  L1: A
  L2: "9"
  L3:
    P1: F2
    P2: F3
    P3: F1
  
  # Reading
  R1: C
  R2: [varies by student]
  R3: [varies by student]
  
  # Grammar & Vocabulary
  GV1: B
  GV2: make
  GV3:
    P1: D3
    P2: F2
    P3: O1
  GV4: A

# Speaking and Writing use rubrics for scoring
subjective_items:
  S1: 
    criteria: [pronunciation, fluency, accuracy]
    max_score: 5
  S2:
    criteria: [content, vocabulary, grammar, fluency]
    max_score: 10
  S3:
    criteria: [appropriateness, clarity, language]
    max_score: 10
  S4:
    criteria: [content, organization, vocabulary, grammar]
    max_score: 15
  
  W1:
    criteria: [task_achievement, vocabulary, grammar, spelling_punctuation]
    max_score: 5
  W2:
    criteria: [completeness, accuracy, capitalization]
    max_score: 5
  W3:
    criteria: [task_achievement, organization, vocabulary, grammar]
    max_score: 10
```

## 7. Scoring Rubrics

```yaml
# rubric.yaml
rubrics:
  # Speaking Rubrics
  speaking_read_aloud:
    max_score: 5
    criteria:
      pronunciation:
        weight: 40
        levels:
          - score: 5
            description: "All words pronounced clearly and correctly"
          - score: 4
            description: "Most words pronounced correctly, minor errors"
          - score: 3
            description: "Some pronunciation errors but understandable"
          - score: 2
            description: "Many pronunciation errors, sometimes unclear"
          - score: 1
            description: "Very difficult to understand"
      
      fluency:
        weight: 40
        levels:
          - score: 5
            description: "Natural pace and rhythm, appropriate pauses"
          - score: 4
            description: "Generally fluent with minor hesitations"
          - score: 3
            description: "Some hesitations but maintains flow"
          - score: 2
            description: "Frequent pauses, slow or rushed"
          - score: 1
            description: "Very slow with long pauses or extremely rushed"
      
      accuracy:
        weight: 20
        levels:
          - score: 5
            description: "Reads entire text correctly"
          - score: 4
            description: "Misses or changes 1-2 words"
          - score: 3
            description: "Misses or changes 3-4 words"
          - score: 2
            description: "Misses or changes 5-6 words"
          - score: 1
            description: "Misses or changes more than 6 words"

  # Writing Rubrics
  writing_short_message:
    max_score: 5
    criteria:
      task_achievement:
        weight: 30
        levels:
          - score: 5
            description: "Includes all three required points clearly"
          - score: 4
            description: "Includes all three points, one may be unclear"
          - score: 3
            description: "Includes two points clearly"
          - score: 2
            description: "Includes only one point or two unclear"
          - score: 1
            description: "Missing or very unclear points"
      
      vocabulary:
        weight: 25
        levels:
          - score: 5
            description: "Appropriate holiday vocabulary, 20-40 words"
          - score: 4
            description: "Good vocabulary, minor word choice issues"
          - score: 3
            description: "Adequate vocabulary, some repetition"
          - score: 2
            description: "Limited vocabulary, frequent repetition"
          - score: 1
            description: "Very limited vocabulary or incorrect usage"
      
      grammar:
        weight: 25
        levels:
          - score: 5
            description: "Present simple used correctly throughout"
          - score: 4
            description: "Minor grammar errors, meaning clear"
          - score: 3
            description: "Some grammar errors but understandable"
          - score: 2
            description: "Frequent grammar errors, sometimes unclear"
          - score: 1
            description: "Very poor grammar, difficult to understand"
      
      spelling_punctuation:
        weight: 20
        levels:
          - score: 5
            description: "All common words spelled correctly"
          - score: 4
            description: "1-2 spelling or punctuation errors"
          - score: 3
            description: "3-4 spelling or punctuation errors"
          - score: 2
            description: "5-6 errors affecting readability"
          - score: 1
            description: "Many errors making text hard to read"

# Total Section Weights and Scoring

section_scoring:
  listening:
    items: 8-10
    raw_score: 8-10 points
    weight: 25%
    
  reading:
    items: 5-7
    raw_score: 5-7 points
    weight: 20%
    
  grammar_vocabulary:
    items: 10-12
    raw_score: 10-12 points
    weight: 20%
    
  speaking:
    tasks: 3-4
    raw_score: 30-40 points
    scaled_to: 25 points
    weight: 25%
    
  writing:
    tasks: 1-2
    raw_score: 15 points
    scaled_to: 10 points
    weight: 10%

# Final Score Calculation
final_score:
  max_raw_score: 100
  passing_threshold: 60%
  
  grade_boundaries:
    A: 90-100
    B: 80-89
    C: 70-79
    D: 60-69
    F: 0-59
```

---

## Ringkasan A1 Content Schema

### Statistik Total
- **Total Items**: 35-42 items
- **Duration**: 45 menit
- **Max Score**: 100 points
- **Passing**: 60%

### Breakdown per Section
1. **Listening**: 8-10 items (25%)
   - MCQ, Fill-in-blank, Matching
   
2. **Reading**: 5-7 items (20%)
   - MCQ, Fill-in-blank
   
3. **Grammar & Vocabulary**: 10-12 items (20%)
   - MCQ, Fill-in-blank, Matching
   
4. **Speaking**: 3-4 tasks (25%)
   - Read aloud, Short response, Situational response, Extended response
   
5. **Writing**: 1-2 tasks (10%)
   - Short message, Form filling, Guided writing

### File yang Sudah Dibuat
1. `blueprint.yaml` - Konfigurasi exam
2. `audio_manifest.yaml` - Asset audio listening
3. `items/listening.yaml` - 3 contoh items listening
4. `items/reading.yaml` - 3 contoh items reading
5. `items/grammar_vocabulary.yaml` - 4 contoh items grammar/vocab
6. `items/speaking.yaml` - 4 contoh tasks speaking
7. `items/writing.yaml` - 3 contoh tasks writing
8. `answer_key.yaml` - Kunci jawaban objective items
9. `rubric.yaml` - Rubrik scoring lengkap untuk speaking dan writing

Langkah berikutnya: Implementasi database schema dan API berdasarkan spec ini?