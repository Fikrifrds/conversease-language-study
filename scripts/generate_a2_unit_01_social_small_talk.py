from __future__ import annotations

from pathlib import Path


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    unit_root = (
        repo_root
        / "content"
        / "curriculum"
        / "english"
        / "A2"
        / "units"
        / "unit-01-social-small-talk"
    )

    lessons: dict[str, dict[str, str]] = {
        "lesson-01-starting-small-talk": {
            "lesson.yaml": """lesson_key: lesson-01-starting-small-talk
slug: starting-small-talk
title: Starting Small Talk
status: draft
estimated_minutes: 10
conversation_situation: starting_small_talk_at_work
conversation_goal: Start a short small-talk conversation and keep it going with one follow-up question.
grammar_summary: "Use How's + noun? to ask about someone, and use It was + adjective to talk about the weekend."
required_sections:
  - conversation_goal
  - situation_setup
  - listening
  - comprehension_check
  - useful_phrases
  - grammar_for_conversation
  - speak_clearly
  - response_practice
  - conversation_coach_roleplay
  - conversation_feedback
  - conversation_check
completion_rules:
  listening_completed: true
  quiz_required: true
  speaking_attempt_required: true
  minimum_score: 65
""",
            "lesson.md": """# Starting Small Talk

## Conversation Outcome

After this lesson, learners can start a short small-talk conversation and keep it going with one follow-up question.

## Situation

Kamu bertemu rekan kerja di kantor. Kamu ingin memulai obrolan ringan, tanya kabar, dan tanya satu pertanyaan lanjutan dengan sopan.

## Lesson Flow

1. Listen to a short dialogue.
2. Understand the conversation with Indonesian support.
3. Practice useful small-talk phrases.
4. Repeat key phrases clearly.
5. Respond to short prompts.
6. Practice the same situation with Conversation Coach.
7. Review conversation feedback.
""",
            "conversation_goal.md": """Start a short small-talk conversation and keep it going with one follow-up question.

Learners should be able to say:

- How's your day?
- It's busy today.
- How was your weekend?
- Sounds great.
- Have a good day!
""",
            "listening_script.md": """# Dialogue Script

**Ben:** Hi Mina. How's your day?  
**Mina:** Hi Ben. It's good, thanks. How about you?  
**Ben:** Pretty good. It's busy today.  
**Mina:** Yeah, the office is really busy.  
**Ben:** By the way, how was your weekend?  
**Mina:** It was nice. I went to the park.  
**Ben:** Sounds great. Have a good day!  
**Mina:** You too. See you later.

## Audio Direction

- Level: A2
- Speed: slow and natural
- Tone: friendly, clear, supportive
- Voices: one male colleague, one female colleague
""",
            "transcript_translation.md": """# Transcript Translation

- **Ben:** Hi Mina. How's your day? -> Hai Mina. Gimana harimu?
- **Mina:** Hi Ben. It's good, thanks. How about you? -> Hai Ben. Baik, terima kasih. Kamu gimana?
- **Ben:** Pretty good. It's busy today. -> Lumayan baik. Hari ini sibuk.
- **Mina:** Yeah, the office is really busy. -> Iya, kantor benar-benar sibuk.
- **Ben:** By the way, how was your weekend? -> Oh ya, gimana akhir pekanmu?
- **Mina:** It was nice. I went to the park. -> Menyenangkan. Saya pergi ke taman.
- **Ben:** Sounds great. Have a good day! -> Kedengarannya seru. Semoga harimu menyenangkan!
- **Mina:** You too. See you later. -> Kamu juga. Sampai nanti.
""",
            "useful_phrases.yaml": """phrases:
  - phrase: How's your day?
    meaning_id: Gimana harimu?
    usage_note: Use this to start small talk with someone you know.
    common_mistake: Do not say "How is your day?" in casual conversation unless you want to sound more formal.
  - phrase: Pretty good.
    meaning_id: Lumayan baik.
    usage_note: A casual, positive answer to a "How are you?" question.
    common_mistake: Do not confuse "pretty" here with physical appearance.
  - phrase: It's busy today.
    meaning_id: Hari ini sibuk.
    usage_note: Use this to explain your day in a simple way.
    common_mistake: Do not say "busy is today".
  - phrase: By the way,
    meaning_id: Oh ya,
    usage_note: Use this before changing the topic slightly.
    common_mistake: Do not overuse it in every sentence.
  - phrase: How was your weekend?
    meaning_id: Gimana akhir pekanmu?
    usage_note: Ask this on Monday or after the weekend.
    common_mistake: Do not say "How is your weekend?" when the weekend is already finished.
  - phrase: Sounds great.
    meaning_id: Kedengarannya seru.
    usage_note: A friendly reaction to good news or a nice plan.
    common_mistake: Do not drop the -s: "Sound great" is incorrect here.
""",
            "grammar_for_conversation.md": """# Grammar for Conversation

Use **How's + noun?** for casual small talk.

Examples:

- How's your day?
- How's work?

Use **It was + adjective** to talk about a finished time in the past.

Examples:

- How was your weekend? It was nice.
- How was the trip? It was great.
""",
            "pronunciation_drill.md": """# Pronunciation Drill

Repeat slowly, then say it in a short answer.

- **How's your day?** - Link it: howz-yer-day.
- **pretty** - Say PRI-tee, not PREH-tee.
- **weekend** - Stress WEE: WEE-kend.
""",
            "response_prompts.yaml": """prompts:
  - prompt: Ask about someone's day.
    target_response: How's your day?
    acceptable_variations:
      - How's your day?
      - How's your day going?
  - prompt: Say that today is busy.
    target_response: It's busy today.
    acceptable_variations:
      - It's busy today.
      - It's really busy today.
  - prompt: Ask about the weekend.
    target_response: How was your weekend?
    acceptable_variations:
      - How was your weekend?
""",
            "conversation_coach_roleplay.yaml": """scenario_key: a2_small_talk_at_work
mode: lesson_practice_coach
level_code: A2
opening_line: Hi! How's your day?
learner_goal: Start small talk, answer naturally, and ask one follow-up question before closing politely.
max_turns: 8
feedback_level:
  free: basic
  pro: detailed
target_phrases:
  - How's your day?
  - It's busy today.
  - How was your weekend?
  - Sounds great.
rubric:
  speaking:
    minimum_score: 65
  relevance:
    minimum_score: 65
  grammar:
    minimum_score: 60
""",
            "quiz.yaml": """questions:
  - key: meaning_hows_your_day
    type: multiple_choice
    prompt: What does "How's your day?" mean?
    options:
      - Gimana harimu?
      - Jam berapa sekarang?
      - Kamu dari mana?
    correct_answer: Gimana harimu?
  - key: follow_up_weekend
    type: multiple_choice
    prompt: Which is the best follow-up question about the weekend?
    options:
      - How was your weekend?
      - How are you weekend?
      - How do you weekend?
    correct_answer: How was your weekend?
  - key: reaction_sounds_great
    type: multiple_choice
    prompt: What is a natural reaction to "I went to the park"?
    options:
      - Sounds great.
      - Good night.
      - I'm sorry.
    correct_answer: Sounds great.
""",
            "reading_support.md": """# Reading Support

Ben meets Mina at the office. He asks about her day and her weekend. Mina says her weekend was nice and she went to the park.

## Check

Read it again and underline the small-talk question.
""",
            "writing_support.md": """# Writing Support

Write 3 short sentences:

1. Say hello.
2. Ask about the day or the weekend.
3. Close politely.
""",
            "audio_manifest.yaml": """lesson_key: lesson-01-starting-small-talk
status: not_generated
provider: minimax
model: speech-2.8-hd
default_voice_id: multi_speaker
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url:
    duration_seconds:
    provider: minimax
    model: speech-2.8-hd
    voice_id: multi_speaker
    speaker_voices:
      Ben: English_Gentle-voiced_man
      Mina: English_Upbeat_Woman
  - key: phrases
    type: phrase_pronunciation
    source_file: useful_phrases.yaml
    audio_url:
    duration_seconds:
""",
        },
        "lesson-02-asking-follow-up-questions": {
            "lesson.yaml": """lesson_key: lesson-02-asking-follow-up-questions
slug: asking-follow-up-questions
title: Asking Follow-up Questions
status: draft
estimated_minutes: 10
conversation_situation: asking_follow_up_questions_in_small_talk
conversation_goal: Ask simple follow-up questions to keep a conversation going.
grammar_summary: "Use Where is it? and What did you + verb? for follow-up questions about place and past actions."
required_sections:
  - conversation_goal
  - situation_setup
  - listening
  - comprehension_check
  - useful_phrases
  - grammar_for_conversation
  - speak_clearly
  - response_practice
  - conversation_coach_roleplay
  - conversation_feedback
  - conversation_check
completion_rules:
  listening_completed: true
  quiz_required: true
  speaking_attempt_required: true
  minimum_score: 65
""",
            "lesson.md": """# Asking Follow-up Questions

## Conversation Outcome

After this lesson, learners can ask simple follow-up questions to keep a conversation going.

## Situation

Temanmu cerita tentang sesuatu yang dia lakukan kemarin. Kamu ingin bertanya lebih lanjut: di mana, apa yang dia lakukan, dan bagaimana hasilnya.

## Lesson Flow

1. Listen to a short dialogue.
2. Understand the conversation with Indonesian support.
3. Practice useful follow-up questions.
4. Repeat key phrases clearly.
5. Respond to short prompts.
6. Practice the same situation with Conversation Coach.
7. Review conversation feedback.
""",
            "conversation_goal.md": """Ask simple follow-up questions to keep a conversation going.

Learners should be able to say:

- Where is it?
- What did you order?
- Was it good?
- Do you want to go sometime?
- That sounds fun.
""",
            "listening_script.md": """# Dialogue Script

**Adi:** Hi Lina. I went to a new cafe yesterday.  
**Lina:** Oh, nice! Where is it?  
**Adi:** It's near the station.  
**Lina:** What did you order?  
**Adi:** I ordered iced coffee.  
**Lina:** Was it good?  
**Adi:** Yes, it was great. Do you want to go sometime?  
**Lina:** Sure! That sounds fun.

## Audio Direction

- Level: A2
- Speed: slow and natural
- Tone: friendly, curious, supportive
- Voices: two young adults, clear pronunciation
""",
            "transcript_translation.md": """# Transcript Translation

- **Adi:** Hi Lina. I went to a new cafe yesterday. -> Hai Lina. Saya pergi ke kafe baru kemarin.
- **Lina:** Oh, nice! Where is it? -> Oh, seru! Di mana itu?
- **Adi:** It's near the station. -> Itu dekat stasiun.
- **Lina:** What did you order? -> Kamu pesan apa?
- **Adi:** I ordered iced coffee. -> Saya pesan es kopi.
- **Lina:** Was it good? -> Enak tidak?
- **Adi:** Yes, it was great. Do you want to go sometime? -> Iya, enak banget. Kamu mau pergi bareng kapan-kapan?
- **Lina:** Sure! That sounds fun. -> Boleh! Kedengarannya seru.
""",
            "useful_phrases.yaml": """phrases:
  - phrase: Where is it?
    meaning_id: Di mana itu?
    usage_note: Ask about the location of a place someone mentions.
    common_mistake: Do not say "Where it is?" in a normal question.
  - phrase: What did you order?
    meaning_id: Kamu pesan apa?
    usage_note: Ask what someone bought or asked for at a cafe or restaurant.
    common_mistake: Do not say "What you ordered?" without did.
  - phrase: Was it good?
    meaning_id: Enak tidak?
    usage_note: Ask if the experience or food was good.
    common_mistake: Use was for the past. Do not say "Is it good?" if it already happened.
  - phrase: Do you want to go sometime?
    meaning_id: Kamu mau pergi bareng kapan-kapan?
    usage_note: A casual invitation without a fixed time.
    common_mistake: Do not say "Do you want go" without to.
  - phrase: That sounds fun.
    meaning_id: Kedengarannya seru.
    usage_note: A positive reaction to a plan or idea.
    common_mistake: Do not say "sound fun" without -s.
""",
            "grammar_for_conversation.md": """# Grammar for Conversation

Use **Where is it?** to ask about the location.

Examples:

- I found a new cafe. Where is it?
- There's a good shop. Where is it?

Use **What did you + verb?** for follow-up questions about the past.

Examples:

- What did you order?
- What did you eat?
""",
            "pronunciation_drill.md": """# Pronunciation Drill

Repeat slowly, then say it in a short answer.

- **yesterday** - Stress YES: YES-ter-day.
- **ordered** - Say OR-derd, not OR-der-ed.
- **sometime** - Link it smoothly: SUM-time.
""",
            "response_prompts.yaml": """prompts:
  - prompt: Ask where the cafe is.
    target_response: Where is it?
    acceptable_variations:
      - Where is it?
      - Where is the cafe?
  - prompt: Ask what they ordered.
    target_response: What did you order?
    acceptable_variations:
      - What did you order?
  - prompt: Invite someone casually.
    target_response: Do you want to go sometime?
    acceptable_variations:
      - Do you want to go sometime?
      - Do you want to go together sometime?
""",
            "conversation_coach_roleplay.yaml": """scenario_key: a2_follow_up_questions_cafe
mode: lesson_practice_coach
level_code: A2
opening_line: I went to a new cafe yesterday.
learner_goal: Ask two short follow-up questions and respond with a natural reaction.
max_turns: 9
feedback_level:
  free: basic
  pro: detailed
target_phrases:
  - Where is it?
  - What did you order?
  - Was it good?
  - That sounds fun.
rubric:
  speaking:
    minimum_score: 65
  relevance:
    minimum_score: 65
  grammar:
    minimum_score: 60
""",
            "quiz.yaml": """questions:
  - key: follow_up_location
    type: multiple_choice
    prompt: Which question asks about the location?
    options:
      - Where is it?
      - Was it good?
      - What did you order?
    correct_answer: Where is it?
  - key: past_follow_up
    type: multiple_choice
    prompt: Which is the correct follow-up question about the past?
    options:
      - What did you order?
      - What you ordered?
      - What do you ordered?
    correct_answer: What did you order?
  - key: reaction_fun
    type: multiple_choice
    prompt: What is a natural reaction to an invitation?
    options:
      - That sounds fun.
      - Where is it?
      - I'm sorry to hear that.
    correct_answer: That sounds fun.
""",
            "reading_support.md": """# Reading Support

Adi went to a new cafe yesterday. Lina asks where it is and what Adi ordered. Adi says the cafe is near the station and the iced coffee was great.

## Check

Read it again and find two follow-up questions.
""",
            "writing_support.md": """# Writing Support

Write 3 short follow-up questions you can ask a friend:

- About the place
- About what they did
- About how it was
""",
            "audio_manifest.yaml": """lesson_key: lesson-02-asking-follow-up-questions
status: not_generated
provider: minimax
model: speech-2.8-hd
default_voice_id: multi_speaker
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url:
    duration_seconds:
    provider: minimax
    model: speech-2.8-hd
    voice_id: multi_speaker
    speaker_voices:
      Adi: English_Diligent_Man
      Lina: English_Upbeat_Woman
  - key: phrases
    type: phrase_pronunciation
    source_file: useful_phrases.yaml
    audio_url:
    duration_seconds:
""",
        },
        "lesson-03-talking-about-weekends": {
            "lesson.yaml": """lesson_key: lesson-03-talking-about-weekends
slug: talking-about-weekends
title: Talking About Weekends
status: draft
estimated_minutes: 10
conversation_situation: talking_about_weekend_plans
conversation_goal: Ask about weekend plans and answer with simple details.
grammar_summary: "Use Any plans for the weekend? to ask, and use I'm going to + verb to talk about your plan."
required_sections:
  - conversation_goal
  - situation_setup
  - listening
  - comprehension_check
  - useful_phrases
  - grammar_for_conversation
  - speak_clearly
  - response_practice
  - conversation_coach_roleplay
  - conversation_feedback
  - conversation_check
completion_rules:
  listening_completed: true
  quiz_required: true
  speaking_attempt_required: true
  minimum_score: 65
""",
            "lesson.md": """# Talking About Weekends

## Conversation Outcome

After this lesson, learners can ask about weekend plans and answer with simple details.

## Situation

Kamu ngobrol sebentar dengan teman. Kamu ingin tanya rencana akhir pekan, dan kamu juga bisa menjawab dengan rencana sederhana.

## Lesson Flow

1. Listen to a short dialogue.
2. Understand the conversation with Indonesian support.
3. Practice useful weekend phrases.
4. Repeat key phrases clearly.
5. Respond to short prompts.
6. Practice the same situation with Conversation Coach.
7. Review conversation feedback.
""",
            "conversation_goal.md": """Ask about weekend plans and answer with simple details.

Learners should be able to say:

- Any plans for the weekend?
- I'm going to visit my parents.
- Where do they live?
- How are you getting there?
- I'm taking the train.
""",
            "listening_script.md": """# Dialogue Script

**Dimas:** Hi Alya. Any plans for the weekend?  
**Alya:** Yes. I'm going to visit my parents.  
**Dimas:** Nice. Where do they live?  
**Alya:** They live in Bandung.  
**Dimas:** How are you getting there?  
**Alya:** I'm taking the train on Saturday morning.  
**Dimas:** Sounds good. Have a great weekend.  
**Alya:** Thanks! You too.

## Audio Direction

- Level: A2
- Speed: slow and natural
- Tone: friendly, relaxed, supportive
- Voices: two adults, clear pronunciation
""",
            "transcript_translation.md": """# Transcript Translation

- **Dimas:** Hi Alya. Any plans for the weekend? -> Hai Alya. Ada rencana untuk akhir pekan?
- **Alya:** Yes. I'm going to visit my parents. -> Iya. Saya mau mengunjungi orang tua saya.
- **Dimas:** Nice. Where do they live? -> Seru. Mereka tinggal di mana?
- **Alya:** They live in Bandung. -> Mereka tinggal di Bandung.
- **Dimas:** How are you getting there? -> Kamu ke sana naik apa?
- **Alya:** I'm taking the train on Saturday morning. -> Saya naik kereta hari Sabtu pagi.
- **Dimas:** Sounds good. Have a great weekend. -> Kedengarannya bagus. Semoga akhir pekanmu menyenangkan.
- **Alya:** Thanks! You too. -> Terima kasih! Kamu juga.
""",
            "useful_phrases.yaml": """phrases:
  - phrase: Any plans for the weekend?
    meaning_id: Ada rencana untuk akhir pekan?
    usage_note: A casual way to ask about weekend plans.
    common_mistake: Do not say "Any plan for weekend?" without the -s.
  - phrase: I'm going to visit my parents.
    meaning_id: Saya mau mengunjungi orang tua saya.
    usage_note: Use going to to talk about a plan.
    common_mistake: Do not say "I going to".
  - phrase: Where do they live?
    meaning_id: Mereka tinggal di mana?
    usage_note: Ask where someone's parents or friends live.
    common_mistake: Do not say "Where they live?" without do.
  - phrase: How are you getting there?
    meaning_id: Kamu ke sana naik apa?
    usage_note: Ask about transport to a place.
    common_mistake: Do not say "How you get there?"
  - phrase: Have a great weekend.
    meaning_id: Semoga akhir pekanmu menyenangkan.
    usage_note: A friendly closing on Friday or before the weekend.
    common_mistake: Do not say "Have great weekend" without a.
""",
            "grammar_for_conversation.md": """# Grammar for Conversation

Use **Any plans for ...?** to ask casually.

Examples:

- Any plans for the weekend?
- Any plans for tonight?

Use **I'm going to + verb** to talk about a plan.

Examples:

- I'm going to visit my parents.
- I'm going to take the train.
""",
            "pronunciation_drill.md": """# Pronunciation Drill

Repeat slowly, then say it in a short answer.

- **going to** - Say GON-na in fast speech: I'm gonna visit my parents.
- **weekend** - Stress WEE: WEE-kend.
- **parents** - Stress PAR: PAR-ents.
""",
            "response_prompts.yaml": """prompts:
  - prompt: Ask about weekend plans.
    target_response: Any plans for the weekend?
    acceptable_variations:
      - Any plans for the weekend?
      - Do you have any plans for the weekend?
  - prompt: Say you are going to visit your parents.
    target_response: I'm going to visit my parents.
    acceptable_variations:
      - I'm going to visit my parents.
  - prompt: Ask about transport.
    target_response: How are you getting there?
    acceptable_variations:
      - How are you getting there?
      - How will you get there?
""",
            "conversation_coach_roleplay.yaml": """scenario_key: a2_weekend_plans_chat
mode: lesson_practice_coach
level_code: A2
opening_line: Any plans for the weekend?
learner_goal: Say your plan with one detail, answer one follow-up question, and close politely.
max_turns: 9
feedback_level:
  free: basic
  pro: detailed
target_phrases:
  - Any plans for the weekend?
  - I'm going to visit my parents.
  - How are you getting there?
  - Have a great weekend.
rubric:
  speaking:
    minimum_score: 65
  relevance:
    minimum_score: 65
  grammar:
    minimum_score: 60
""",
            "quiz.yaml": """questions:
  - key: ask_weekend_plans
    type: multiple_choice
    prompt: Which question asks about weekend plans?
    options:
      - Any plans for the weekend?
      - Where do you live?
      - What time is it?
    correct_answer: Any plans for the weekend?
  - key: going_to_plan
    type: multiple_choice
    prompt: Which sentence uses going to to talk about a plan?
    options:
      - I'm going to visit my parents.
      - I visited my parents.
      - I'm visit my parents.
    correct_answer: I'm going to visit my parents.
  - key: transport_question
    type: multiple_choice
    prompt: Which question asks about transport?
    options:
      - How are you getting there?
      - Where are you?
      - Are you busy?
    correct_answer: How are you getting there?
""",
            "reading_support.md": """# Reading Support

Alya is going to visit her parents this weekend. They live in Bandung. She is taking the train on Saturday morning.

## Check

Read it again and circle the plan and the time.
""",
            "writing_support.md": """# Writing Support

Write 3 short sentences about your weekend plan:

1. Say your plan using going to.
2. Add one place.
3. Add one time.
""",
            "audio_manifest.yaml": """lesson_key: lesson-03-talking-about-weekends
status: not_generated
provider: minimax
model: speech-2.8-hd
default_voice_id: multi_speaker
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url:
    duration_seconds:
    provider: minimax
    model: speech-2.8-hd
    voice_id: multi_speaker
    speaker_voices:
      Dimas: English_Diligent_Man
      Alya: English_radiant_girl
  - key: phrases
    type: phrase_pronunciation
    source_file: useful_phrases.yaml
    audio_url:
    duration_seconds:
""",
        },
        "lesson-04-reacting-politely": {
            "lesson.yaml": """lesson_key: lesson-04-reacting-politely
slug: reacting-politely
title: Reacting Politely
status: draft
estimated_minutes: 10
conversation_situation: reacting_politely_in_small_talk
conversation_goal: React politely to good news and to a small problem.
grammar_summary: "Use I'm sorry to hear that for a small problem, and use That's great! for good news."
required_sections:
  - conversation_goal
  - situation_setup
  - listening
  - comprehension_check
  - useful_phrases
  - grammar_for_conversation
  - speak_clearly
  - response_practice
  - conversation_coach_roleplay
  - conversation_feedback
  - conversation_check
completion_rules:
  listening_completed: true
  quiz_required: true
  speaking_attempt_required: true
  minimum_score: 65
""",
            "lesson.md": """# Reacting Politely

## Conversation Outcome

After this lesson, learners can react politely to good news and to a small problem.

## Situation

Kamu ngobrol singkat dengan teman. Temanmu bilang dia capek. Kamu merespons dengan sopan, lalu temanmu juga cerita kabar baik.

## Lesson Flow

1. Listen to a short dialogue.
2. Understand the conversation with Indonesian support.
3. Practice useful reaction phrases.
4. Repeat key phrases clearly.
5. Respond to short prompts.
6. Practice the same situation with Conversation Coach.
7. Review conversation feedback.
""",
            "conversation_goal.md": """React politely to good news and to a small problem.

Learners should be able to say:

- I'm a bit tired today.
- Are you okay?
- I'm sorry to hear that.
- That's great!
- Nice work.
""",
            "listening_script.md": """# Dialogue Script

**Mina:** Hi Ben. I'm a bit tired today.  
**Ben:** Oh no. Are you okay?  
**Mina:** Yeah, I'm fine. I didn't sleep well.  
**Ben:** I'm sorry to hear that.  
**Mina:** It's okay. How about you?  
**Ben:** I'm good. I finished my project.  
**Mina:** That's great! Nice work.  
**Ben:** Thanks!

## Audio Direction

- Level: A2
- Speed: slow and natural
- Tone: friendly, warm, supportive
- Voices: one female colleague, one male colleague
""",
            "transcript_translation.md": """# Transcript Translation

- **Mina:** Hi Ben. I'm a bit tired today. -> Hai Ben. Saya agak capek hari ini.
- **Ben:** Oh no. Are you okay? -> Oh tidak. Kamu tidak apa-apa?
- **Mina:** Yeah, I'm fine. I didn't sleep well. -> Iya, saya baik-baik saja. Saya kurang tidur.
- **Ben:** I'm sorry to hear that. -> Saya ikut sedih dengarnya.
- **Mina:** It's okay. How about you? -> Tidak apa-apa. Kalau kamu gimana?
- **Ben:** I'm good. I finished my project. -> Saya baik. Saya sudah menyelesaikan proyek saya.
- **Mina:** That's great! Nice work. -> Keren! Kerja bagus.
- **Ben:** Thanks! -> Terima kasih!
""",
            "useful_phrases.yaml": """phrases:
  - phrase: I'm a bit tired today.
    meaning_id: Saya agak capek hari ini.
    usage_note: Use a bit to sound softer and more natural.
    common_mistake: Do not say "I bit tired".
  - phrase: Are you okay?
    meaning_id: Kamu tidak apa-apa?
    usage_note: Use this to check if someone is fine.
    common_mistake: Do not say "Are you ok?" too aggressively; keep a friendly tone.
  - phrase: I didn't sleep well.
    meaning_id: Saya kurang tidur.
    usage_note: A simple way to explain why you are tired.
    common_mistake: Do not say "I no sleep well".
  - phrase: I'm sorry to hear that.
    meaning_id: Saya ikut sedih dengarnya.
    usage_note: A polite reaction to bad news or a small problem.
    common_mistake: Do not say this for good news.
  - phrase: That's great!
    meaning_id: Keren!
    usage_note: A positive reaction to good news.
    common_mistake: Keep the intonation positive.
  - phrase: Nice work.
    meaning_id: Kerja bagus.
    usage_note: Use this to compliment someone.
    common_mistake: Do not say "Nice working" here.
""",
            "grammar_for_conversation.md": """# Grammar for Conversation

Use **I'm a bit + adjective** to sound natural.

Examples:

- I'm a bit tired today.
- I'm a bit busy right now.

Use **didn't + base verb** for a negative in the simple past.

Examples:

- I didn't sleep well.
- I didn't go out yesterday.
""",
            "pronunciation_drill.md": """# Pronunciation Drill

Repeat slowly, then say it in a short answer.

- **tired** - Say TAI-erd, not TI-red.
- **didn't** - Keep it short: DID-nt.
- **sorry** - Stress SOR: SOR-ree.
""",
            "response_prompts.yaml": """prompts:
  - prompt: Say you are a bit tired.
    target_response: I'm a bit tired today.
    acceptable_variations:
      - I'm a bit tired today.
      - I'm a little tired today.
  - prompt: Check if someone is okay.
    target_response: Are you okay?
    acceptable_variations:
      - Are you okay?
      - Are you alright?
  - prompt: React politely to bad news.
    target_response: I'm sorry to hear that.
    acceptable_variations:
      - I'm sorry to hear that.
""",
            "conversation_coach_roleplay.yaml": """scenario_key: a2_polite_reactions_chat
mode: lesson_practice_coach
level_code: A2
opening_line: I'm a bit tired today.
learner_goal: React politely, ask one short follow-up question, and respond to one piece of good news.
max_turns: 10
feedback_level:
  free: basic
  pro: detailed
target_phrases:
  - Are you okay?
  - I'm sorry to hear that.
  - That's great!
  - Nice work.
rubric:
  speaking:
    minimum_score: 65
  relevance:
    minimum_score: 65
  grammar:
    minimum_score: 60
""",
            "quiz.yaml": """questions:
  - key: reaction_bad_news
    type: multiple_choice
    prompt: Which phrase is a polite reaction to bad news?
    options:
      - I'm sorry to hear that.
      - That's great!
      - See you later.
    correct_answer: I'm sorry to hear that.
  - key: reaction_good_news
    type: multiple_choice
    prompt: Which phrase is a natural reaction to "I finished my project"?
    options:
      - That's great!
      - I'm sorry to hear that.
      - Where is it?
    correct_answer: That's great!
  - key: past_negative
    type: multiple_choice
    prompt: Choose the correct sentence.
    options:
      - I didn't sleep well.
      - I didn't slept well.
      - I don't slept well.
    correct_answer: I didn't sleep well.
""",
            "reading_support.md": """# Reading Support

Mina is tired today because she didn't sleep well. Ben reacts politely. Then Ben shares good news: he finished his project, and Mina reacts positively.

## Check

Read it again and find one reaction to bad news and one reaction to good news.
""",
            "writing_support.md": """# Writing Support

Write 4 short sentences:

1. Say you are tired or busy.
2. Explain why (one simple reason).
3. Share one piece of good news.
4. React politely.
""",
            "audio_manifest.yaml": """lesson_key: lesson-04-reacting-politely
status: not_generated
provider: minimax
model: speech-2.8-hd
default_voice_id: multi_speaker
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url:
    duration_seconds:
    provider: minimax
    model: speech-2.8-hd
    voice_id: multi_speaker
    speaker_voices:
      Mina: English_Upbeat_Woman
      Ben: English_Gentle-voiced_man
  - key: phrases
    type: phrase_pronunciation
    source_file: useful_phrases.yaml
    audio_url:
    duration_seconds:
""",
        },
        "lesson-05-small-talk-mission": {
            "lesson.yaml": """lesson_key: lesson-05-small-talk-mission
slug: small-talk-mission
title: Small Talk Mission
status: draft
estimated_minutes: 12
conversation_situation: small_talk_mission_make_a_plan
conversation_goal: Start small talk, ask follow-up questions, react politely, and make a simple weekend plan.
grammar_summary: "Combine small-talk questions with simple past and going to for a short plan."
required_sections:
  - conversation_goal
  - situation_setup
  - listening
  - comprehension_check
  - useful_phrases
  - grammar_for_conversation
  - speak_clearly
  - response_practice
  - conversation_coach_roleplay
  - conversation_feedback
  - conversation_check
completion_rules:
  listening_completed: true
  quiz_required: true
  speaking_attempt_required: true
  minimum_score: 70
""",
            "lesson.md": """# Small Talk Mission

## Conversation Outcome

After this mission, learners can start small talk, ask follow-up questions, react politely, and make a simple weekend plan.

## Situation

Ini misi gabungan Unit 1. Kamu ngobrol singkat dengan teman, tanya kabar, tanya lebih lanjut, lalu buat rencana sederhana untuk akhir pekan.

## Lesson Flow

1. Listen to a short dialogue.
2. Understand the conversation with Indonesian support.
3. Practice key phrases from the mission.
4. Repeat key phrases clearly.
5. Respond to short prompts.
6. Practice the same situation with Conversation Coach.
7. Review conversation feedback.
""",
            "conversation_goal.md": """Start small talk, ask follow-up questions, react politely, and make a simple weekend plan.

Learners should be able to say:

- How's it going?
- Did you sleep well?
- I'm sorry to hear that.
- Any plans for the weekend?
- Do you want to join?
""",
            "listening_script.md": """# Dialogue Script

**Ben:** Hi Lina. How's it going?  
**Lina:** Hi Ben. I'm good, thanks. How about you?  
**Ben:** I'm a bit tired today.  
**Lina:** Oh no. Did you sleep well?  
**Ben:** Not really. I stayed up late.  
**Lina:** I'm sorry to hear that.  
**Ben:** It's okay. By the way, any plans for the weekend?  
**Lina:** Yes. I'm going to a new cafe. Do you want to join?  
**Ben:** That sounds fun. What time?  
**Lina:** Saturday at 3 pm.  
**Ben:** Great. See you then!  
**Lina:** See you!

## Audio Direction

- Level: A2
- Speed: slow and natural
- Tone: friendly, supportive, confident
- Voices: one male friend, one female friend
""",
            "transcript_translation.md": """# Transcript Translation

- **Ben:** Hi Lina. How's it going? -> Hai Lina. Gimana kabarmu?
- **Lina:** Hi Ben. I'm good, thanks. How about you? -> Hai Ben. Saya baik, terima kasih. Kamu gimana?
- **Ben:** I'm a bit tired today. -> Saya agak capek hari ini.
- **Lina:** Oh no. Did you sleep well? -> Oh tidak. Kamu tidur nyenyak?
- **Ben:** Not really. I stayed up late. -> Tidak juga. Saya begadang.
- **Lina:** I'm sorry to hear that. -> Saya ikut sedih dengarnya.
- **Ben:** It's okay. By the way, any plans for the weekend? -> Tidak apa-apa. Oh ya, ada rencana untuk akhir pekan?
- **Lina:** Yes. I'm going to a new cafe. Do you want to join? -> Iya. Saya mau ke kafe baru. Kamu mau ikut?
- **Ben:** That sounds fun. What time? -> Kedengarannya seru. Jam berapa?
- **Lina:** Saturday at 3 pm. -> Sabtu jam 3 sore.
- **Ben:** Great. See you then! -> Oke. Sampai ketemu nanti!
- **Lina:** See you! -> Sampai jumpa!
""",
            "useful_phrases.yaml": """phrases:
  - phrase: How's it going?
    meaning_id: Gimana kabarmu?
    usage_note: A casual way to ask how someone is.
    common_mistake: Do not answer with only yes or no.
  - phrase: Did you sleep well?
    meaning_id: Kamu tidur nyenyak?
    usage_note: Ask this if someone says they are tired.
    common_mistake: Do not say "Did you slept well?"
  - phrase: I stayed up late.
    meaning_id: Saya begadang.
    usage_note: A simple reason for being tired.
    common_mistake: Do not say "I stay up late" for the past.
  - phrase: Any plans for the weekend?
    meaning_id: Ada rencana untuk akhir pekan?
    usage_note: A casual question to start a weekend plan conversation.
    common_mistake: Do not say "Any plan for weekend?" without the -s.
  - phrase: Do you want to join?
    meaning_id: Kamu mau ikut?
    usage_note: Invite someone to join an activity.
    common_mistake: Do not say "Do you want join?"
  - phrase: What time?
    meaning_id: Jam berapa?
    usage_note: Ask for the time of a plan.
    common_mistake: In a full sentence, say "What time is it?" or "What time are we meeting?"
""",
            "grammar_for_conversation.md": """# Grammar for Conversation

Use **Did you + base verb?** to ask about the past.

Examples:

- Did you sleep well?
- Did you go out yesterday?

Use **I'm going to + verb** to talk about a plan.

Examples:

- I'm going to a new cafe.
- I'm going to meet a friend.
""",
            "pronunciation_drill.md": """# Pronunciation Drill

Repeat slowly, then say it in a short answer.

- **How's it going?** - Link it: howz-it-GO-ing.
- **stayed up** - Stress STAYED: stayed-UP.
- **Saturday** - Stress SA: SA-ter-day.
""",
            "response_prompts.yaml": """prompts:
  - prompt: Ask how someone is doing.
    target_response: How's it going?
    acceptable_variations:
      - How's it going?
      - How are you doing?
  - prompt: Ask if they slept well.
    target_response: Did you sleep well?
    acceptable_variations:
      - Did you sleep well?
  - prompt: Invite someone to join.
    target_response: Do you want to join?
    acceptable_variations:
      - Do you want to join?
      - Do you want to come with me?
  - prompt: Ask for the time.
    target_response: What time?
    acceptable_variations:
      - What time?
      - What time is it?
""",
            "conversation_coach_roleplay.yaml": """scenario_key: a2_small_talk_mission_make_a_plan
mode: lesson_practice_coach
level_code: A2
opening_line: Hi! How's it going?
learner_goal: Start small talk, ask at least two follow-up questions, and make a simple weekend plan with a time.
max_turns: 12
feedback_level:
  free: basic
  pro: detailed
target_phrases:
  - How's it going?
  - Did you sleep well?
  - I'm sorry to hear that.
  - Any plans for the weekend?
  - Do you want to join?
rubric:
  speaking:
    minimum_score: 70
  relevance:
    minimum_score: 70
  grammar:
    minimum_score: 65
""",
            "quiz.yaml": """questions:
  - key: past_question
    type: multiple_choice
    prompt: Which question is about the past?
    options:
      - Did you sleep well?
      - Do you sleep well?
      - Are you sleep well?
    correct_answer: Did you sleep well?
  - key: invite_join
    type: multiple_choice
    prompt: Which phrase invites someone to join?
    options:
      - Do you want to join?
      - Where is it?
      - I'm sorry to hear that.
    correct_answer: Do you want to join?
  - key: weekend_plan
    type: multiple_choice
    prompt: Which sentence talks about a plan?
    options:
      - I'm going to a new cafe.
      - I go to a new cafe yesterday.
      - I stayed up late tomorrow.
    correct_answer: I'm going to a new cafe.
""",
            "reading_support.md": """# Reading Support

Ben is tired today because he stayed up late. Lina reacts politely. Then Lina suggests a weekend plan: a new cafe on Saturday at 3 pm.

## Check

Read it again and find the reason and the plan time.
""",
            "writing_support.md": """# Writing Support

Write 4 to 5 short sentences for a mission conversation:

1. Say hello and ask how someone is.
2. Say you are tired and give one reason.
3. Ask about weekend plans.
4. Suggest a plan with a time.
5. Close politely.
""",
            "audio_manifest.yaml": """lesson_key: lesson-05-small-talk-mission
status: not_generated
provider: minimax
model: speech-2.8-hd
default_voice_id: multi_speaker
assets:
  - key: dialogue_main
    type: dialogue
    script_file: listening_script.md
    audio_url:
    duration_seconds:
    provider: minimax
    model: speech-2.8-hd
    voice_id: multi_speaker
    speaker_voices:
      Ben: English_Gentle-voiced_man
      Lina: English_Upbeat_Woman
  - key: phrases
    type: phrase_pronunciation
    source_file: useful_phrases.yaml
    audio_url:
    duration_seconds:
""",
        },
    }

    for lesson_key, files in lessons.items():
        lesson_dir = unit_root / lesson_key
        for filename, text in files.items():
            write_text(lesson_dir / filename, text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

