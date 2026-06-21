from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoachTurn:
    coach: str
    hint: str
    sample_answer: str
    focus: str
    expected_keywords: tuple[str, ...] = ()
    indonesian_explanation: str = ""


GENERATED_ROLEPLAY_SCRIPTS: dict[str, tuple[CoachTurn, ...]] = {
    "a1-final-conversation": (
        CoachTurn(coach="Hi, good morning. What is your name?", hint="Perkenalkan diri dengan kalimat lengkap.", sample_answer="Good morning. My name is Faris.", focus="Final opening", expected_keywords=("morning", "name", "faris")),
        CoachTurn(coach="Nice to meet you. Where are you from?", hint="Jawab asal dan tanyakan balik.", sample_answer="I'm from Indonesia. How about you?", focus="Origin and follow-up", expected_keywords=("i'm", "from", "indonesia", "how", "?")),
        CoachTurn(coach="I'm from Malaysia. What do you do every morning?", hint="Sebutkan rutinitas dan waktu.", sample_answer="I study English at seven.", focus="Routine", expected_keywords=("study", "english", "seven")),
        CoachTurn(coach="Great. The cafe is open now.", hint="Tanyakan lokasi cafe.", sample_answer="Where is the cafe?", focus="Place", expected_keywords=("where", "cafe", "?")),
        CoachTurn(coach="Go straight and turn left.", hint="Pesan satu item dengan sopan.", sample_answer="Thank you. I would like one tea, please.", focus="Order", expected_keywords=("one", "tea")),
        CoachTurn(coach="Sure. It is two dollars.", hint="Minta ulang harga jika perlu.", sample_answer="Sorry, can you repeat that, please?", focus="Clarification", expected_keywords=("sorry", "repeat", "?")),
        CoachTurn(coach="Two dollars.", hint="Bayar dan tutup dengan terima kasih.", sample_answer="Here you go. Thank you for your help.", focus="Final closing", expected_keywords=("help",)),
    ),
    "a2-final-conversation": (
        CoachTurn(coach="Hey! How have you been?", hint="Jawab singkat, lalu bilang kabar kamu.", sample_answer="Good. A bit tired, though.", focus="Small talk", expected_keywords=("good", "tired")),
        CoachTurn(coach="Would you recommend the cafe?", hint="Jawab dengan yes + because + reason.", sample_answer="Yes, because the coffee is good and it is quiet.", focus="Recommend with reason", expected_keywords=("because", "coffee")),
        CoachTurn(coach="Nice. Are you free on Saturday afternoon?", hint="Jawab ya/tidak + usulkan waktu.", sample_answer="Yes, I am. Let's meet at 3 p.m.", focus="Confirm plan", expected_keywords=("yes", "meet")),
    ),
    "a2-final-test-practice": (
        CoachTurn(coach="Hi. Ready?", hint="Jawab siap.", sample_answer="Yes, ready.", focus="Start practice", expected_keywords=("yes",)),
        CoachTurn(coach="We haven't had coffee in a while.", hint="Gunakan Do you want to...?", sample_answer="Do you want to grab coffee this weekend?", focus="Invitation", expected_keywords=("want to", "weekend")),
        CoachTurn(coach="Maybe, but you don't look well today.", hint="Gunakan I've had ... for ...", sample_answer="I've had a cough for two days.", focus="Symptom + duration", expected_keywords=("have had", "for")),
    ),
    "accepting-and-declining": (
        CoachTurn(coach="Do you want to join our dinner tonight?", hint="Tolak dengan sopan.", sample_answer="Thanks, but I can't.", focus="Decline politely", expected_keywords=("can't", "thanks")),
        CoachTurn(coach="Oh, okay. Are you busy?", hint="Beri alasan singkat dengan because.", sample_answer="Yes. I'm busy tonight because I have a meeting.", focus="Give a reason", expected_keywords=("i'm busy", "because")),
        CoachTurn(coach="No problem. Maybe another time.", hint="Usulkan waktu lain dengan singkat.", sample_answer="Yes, maybe tomorrow.", focus="Suggest another time", expected_keywords=("maybe", "tomorrow")),
    ),
    "advanced-listening-mission": (
        CoachTurn(coach="Part of me wants to push ahead, but if this fails publicly, we'll lose confidence fast.", hint="It sounds like... Just to check, are you implying...?", sample_answer="It sounds like timing and risk are the main concerns. Just to check, are you implying we should slow down?", focus="Implied meaning", expected_keywords=("sounds like", "just to check", "implying")),
        CoachTurn(coach="Yes, that's close. Given that, how would you summarize it and label the decision?", hint="Let me make sure I got this... The decision is...", sample_answer="Let me make sure I got this: dependencies, time pressure, and visibility. The decision is to propose a phased rollout with clear metrics.", focus="Summary + decision", expected_keywords=("make sure", "decision")),
        CoachTurn(coach="When I say we should be more cautious, what do you think I mean, and what should we do next?", hint="When you say... do you mean... or...? Next steps are...", sample_answer="When you say 'more cautious', do you mean smaller scope or slower timing? Next steps are: I'll send the summary and draft phased options.", focus="Follow-up + next steps", expected_keywords=("do you mean", "next steps")),
    ),
    "advanced-presentation-mission": (
        CoachTurn(coach="Before we get into details, can you frame the proposal and define what you mean by modular architecture?", hint="Today I'd like to... By X, I mean...", sample_answer="Today I'd like to walk you through the proposal and why it matters. By 'modular architecture', I mean independent components.", focus="Framing", expected_keywords=("today", "by", "i mean")),
        CoachTurn(coach="Okay. What's your main claim, what evidence supports it, and what's the main trade-off?", hint="The core claim is... The evidence suggests... That brings me to...", sample_answer="The core claim is that this will improve delivery speed. The evidence suggests teams move faster with clear ownership. That brings me to the key trade-off: speed versus reliability.", focus="Persuasion + transition", expected_keywords=("core claim", "evidence suggests", "trade-off")),
        CoachTurn(coach="Fair question: isn't this going to create extra complexity? How would you answer that, and what are the next steps if we move ahead?", hint="That's a fair question... The short answer is... In short... Next steps are...", sample_answer="That's a fair question. The short answer is: it's manageable if we pilot first and monitor closely. In short, the benefits outweigh the risks if we set guardrails early. Next steps are: I'll share the plan today, and you'll review it by Friday.", focus="Q&A + close", expected_keywords=("fair question", "short answer", "next steps", "by")),
    ),
    "agreeing-and-disagreeing-politely": (
        CoachTurn(coach="I think this restaurant is the best.", hint="Tolak halus + alasan singkat.", sample_answer="I'm not sure. It's a bit expensive.", focus="Soft disagreement with reason", expected_keywords=("not sure", "expensive")),
        CoachTurn(coach="Really? What do you like about it?", hint="Setuju 1 hal, tapi tambah tapi (but).", sample_answer="I agree the food is good, but the service is slow.", focus="Agree and contrast", expected_keywords=("agree", "but")),
        CoachTurn(coach="Okay. Should we try another place next time?", hint="Jawab setuju + That's fair.", sample_answer="Yes, that's fair. Let's try another place.", focus="Accept and plan", expected_keywords=("fair", "try")),
    ),
    "aligning-stakeholders": (
        CoachTurn(coach="We have conflicting priorities across teams.", hint="Mulai dengan alignment question.", sample_answer="To make sure we're aligned, can you share your top priority?", focus="Priorities", expected_keywords=("aligned", "priority")),
        CoachTurn(coach="Our top priority is speed. What do you ask next?", hint="Tanya constraint.", sample_answer="Got it. From your perspective, what's the biggest constraint?", focus="Constraints", expected_keywords=("perspective", "constraint")),
        CoachTurn(coach="We can't add headcount. Close with a decision.", hint="Can we agree that ...", sample_answer="Understood. The key constraint is capacity. Can we agree that we ship a smaller scope first?", focus="Decision", expected_keywords=("key constraint", "agree", "scope")),
    ),
    "answering-questions": (
        CoachTurn(coach="How much effort will this take?", hint="That's a good question. As far as I know...", sample_answer="That's a good question. As far as I know, the first version takes about one day.", focus="Answer with confidence level", expected_keywords=("good question", "as far as I know")),
        CoachTurn(coach="What about maintenance?", hint="I'm not sure yet, but I can follow up...", sample_answer="I'm not sure yet, but I can follow up with an estimate by tomorrow.", focus="Uncertainty + follow up", expected_keywords=("not sure", "follow up")),
        CoachTurn(coach="Who will own it?", hint="I suggest we assign...", sample_answer="I suggest we assign one owner per quarter to keep it updated.", focus="Ownership answer", expected_keywords=("suggest", "assign", "owner")),
    ),
    "apologizing-and-thanking": (
        CoachTurn(coach="Hello, Ben. You are late today.", hint="Minta maaf karena terlambat.", sample_answer="Sorry I'm late.", focus="Apology", expected_keywords=("sorry", "i'm", "late")),
        CoachTurn(coach="That's okay. What happened?", hint="Berikan alasan singkat.", sample_answer="My internet was slow.", focus="Reason", expected_keywords=("internet", "was", "slow")),
        CoachTurn(coach="No problem. Please join the class.", hint="Ucapkan terima kasih sudah menunggu.", sample_answer="Thank you for waiting.", focus="Thanking", expected_keywords=("waiting",)),
        CoachTurn(coach="You're welcome.", hint="Katakan kamu siap sekarang.", sample_answer="I am ready now.", focus="Ready", expected_keywords=("ready",)),
    ),
    "asking-about-culture": (
        CoachTurn(coach="Ask me about a tradition in my country.", hint="Gunakan What is it like...?", sample_answer="What is it like in your country during big holidays?", focus="Ask culture question", expected_keywords=("what is it like", "country")),
        CoachTurn(coach="Answer about your country in 1-2 sentences.", hint="Jawab: It's ... but ... Mostly ...", sample_answer="It's busy, but it's also meaningful. Mostly we share food and spend time together.", focus="Explain briefly", expected_keywords=("busy", "mostly")),
        CoachTurn(coach="Ask back politely.", hint="Gunakan How about in your country?", sample_answer="How about in your country?", focus="Ask back", expected_keywords=("how about",)),
    ),
    "asking-about-departure-time": (
        CoachTurn(coach="Which train?", hint="Sebutkan tujuan keretanya.", sample_answer="The train to Bandung.", focus="Specify the train", expected_keywords=("train", "bandung")),
        CoachTurn(coach="It leaves at 6:30 pm.", hint="Konfirmasi platformnya.", sample_answer="Okay. Which platform?", focus="Ask the platform", expected_keywords=("which platform", "?")),
        CoachTurn(coach="Platform 2.", hint="Tanya durasi perjalanan.", sample_answer="Great. How long is the trip?", focus="Ask the duration", expected_keywords=("how long", "?")),
    ),
    "asking-about-past-activities": (
        CoachTurn(coach="What did you do yesterday evening?", hint="Jawab dengan 1-2 aktivitas (past).", sample_answer="I cooked dinner and listened to music.", focus="Answer with past activities", expected_keywords=("cooked", "listened")),
        CoachTurn(coach="Nice. Did you cook at home?", hint="Jawab singkat.", sample_answer="Yes, I did.", focus="Short past answer", expected_keywords=("did",)),
        CoachTurn(coach="What did you cook?", hint="Sebutkan satu makanan.", sample_answer="I made fried rice.", focus="Answer follow-up", expected_keywords=("made",)),
    ),
    "asking-about-prices": (
        CoachTurn(coach="Hello. Can I help you?", hint="Tanyakan harga coffee.", sample_answer="How much is the coffee?", focus="Price question", expected_keywords=("how", "much", "coffee", "?")),
        CoachTurn(coach="It is two dollars.", hint="Konfirmasi harga.", sample_answer="Two dollars?", focus="Price confirmation", expected_keywords=("two", "dollars", "?")),
        CoachTurn(coach="Yes, two dollars.", hint="Tanyakan harga cake.", sample_answer="How much is the cake?", focus="Second price", expected_keywords=("how", "much", "cake", "?")),
        CoachTurn(coach="It is three dollars.", hint="Tutup dengan thank you.", sample_answer="Okay. Thank you.", focus="Closing", expected_keywords=()),
    ),
    "asking-about-pros-and-cons": (
        CoachTurn(coach="Ask me about pros and cons of this option.", hint="Tanya: What are the pros and cons ...?", sample_answer="What are the pros and cons of working remotely?", focus="Ask about trade-offs", expected_keywords=("pros", "cons")),
        CoachTurn(coach="Give one advantage.", hint="Mulai dengan The advantage is ...", sample_answer="The advantage is you save time.", focus="State an advantage", expected_keywords=("advantage",)),
        CoachTurn(coach="Now give one downside.", hint="Mulai dengan One downside is ...", sample_answer="One downside is you might feel isolated.", focus="State a downside", expected_keywords=("downside", "might")),
    ),
    "asking-about-size-and-color": (
        CoachTurn(coach="Sorry, we don't have black. We have blue and white.", hint="Tanya ukuran yang kamu butuhkan.", sample_answer="Okay. Do you have it in size M?", focus="Ask about size", expected_keywords=("size", "?")),
        CoachTurn(coach="Yes, size M is available.", hint="Pilih salah satu warna.", sample_answer="Great. I'll take the blue one.", focus="Choose an option", expected_keywords=("i'll take", "blue")),
        CoachTurn(coach="Sure.", hint="Tutup dengan sopan.", sample_answer="Thank you.", focus="Close politely", expected_keywords=("thank",)),
    ),
    "asking-about-someones-story": (
        CoachTurn(coach="So you got lost. What happened next?", hint="Jawab dengan 1 aksi di masa lalu.", sample_answer="We asked a local person for help.", focus="Continue the story", expected_keywords=("asked", "help")),
        CoachTurn(coach="Why did you do that?", hint="Jawab dengan because + reason.", sample_answer="Because we did not want to waste time.", focus="Give a reason", expected_keywords=("because",)),
        CoachTurn(coach="How did you feel at that moment?", hint="Sebutkan perasaan (felt...).", sample_answer="I felt worried, but then I felt relieved.", focus="Describe feelings", expected_keywords=("felt", "but")),
    ),
    "asking-about-work-or-study": (
        CoachTurn(coach="Do you work or study?", hint="Jawab apakah kamu bekerja atau belajar.", sample_answer="I study English online.", focus="Work or study", expected_keywords=("study", "english", "online")),
        CoachTurn(coach="What do you do there?", hint="Sebutkan role sederhana.", sample_answer="I'm an assistant.", focus="Simple role", expected_keywords=("i'm", "assistant")),
        CoachTurn(coach="Nice. How about you?", hint="Tanyakan balik dengan How about you?", sample_answer="How about you?", focus="Question back", expected_keywords=("how", "about", "?")),
    ),
    "asking-follow-up-questions": (
        CoachTurn(coach="I went to a new cafe yesterday.", hint="Tanya lokasi atau detailnya dengan pertanyaan singkat.", sample_answer="Oh nice! Where is it?", focus="Ask a follow-up question", expected_keywords=("where is it", "?")),
        CoachTurn(coach="It's near the station.", hint="Tanya apa yang dia pesan atau lakukan di sana.", sample_answer="What did you order?", focus="Ask for details", expected_keywords=("what did you order", "?")),
        CoachTurn(coach="I ordered iced coffee. It was great.", hint="Reaksi positif dan ajak dengan kalimat pendek.", sample_answer="That sounds fun. Do you want to go sometime?", focus="React and invite", expected_keywords=("that sounds fun", "do you want to go")),
    ),
    "asking-for-an-item": (
        CoachTurn(coach="Hi. Can I help you?", hint="Jelaskan barang yang kamu cari.", sample_answer="Yes, please. I'm looking for a phone charger.", focus="Ask for an item", expected_keywords=("i'm looking for", "charger")),
        CoachTurn(coach="Sure. What kind?", hint="Sebutkan jenisnya dengan singkat.", sample_answer="A USB-C charger, please.", focus="Specify the type", expected_keywords=("usb", "charger")),
        CoachTurn(coach="Okay. Do you need a cable too?", hint="Jawab singkat, lalu konfirmasi ketersediaannya.", sample_answer="No, just the charger. Do you have it?", focus="Confirm availability", expected_keywords=("do you have", "?")),
    ),
    "asking-for-clarification": (
        CoachTurn(coach="Can you update the report for Friday?", hint="Terima dulu, lalu minta klarifikasi.", sample_answer="Sure. Could you clarify which sections you need?", focus="Ask for clarification", expected_keywords=("clarify", "sections")),
        CoachTurn(coach="Focus on the summary and the risks.", hint="Konfirmasi satu detail penting.", sample_answer="Got it. Just to confirm, you want the latest numbers too, right?", focus="Confirm details", expected_keywords=("confirm", "latest")),
        CoachTurn(coach="Yes, please include the latest numbers.", hint="Janji deadline singkat.", sample_answer="Okay. I'll send it by Thursday afternoon.", focus="Confirm deadline", expected_keywords=("send", "by")),
    ),
    "asking-for-help": (
        CoachTurn(coach="Hello. Do you need help?", hint="Minta bantuan.", sample_answer="Can you help me?", focus="Help request", expected_keywords=("help", "?")),
        CoachTurn(coach="Sure. What is the problem?", hint="Jelaskan masalah file.", sample_answer="I can't open this file.", focus="Problem statement", expected_keywords=("can't", "open", "file")),
        CoachTurn(coach="Okay. Click this button.", hint="Konfirmasi tombol.", sample_answer="This button?", focus="Instruction check", expected_keywords=("button", "?")),
        CoachTurn(coach="Yes. Try again.", hint="Katakan berhasil dan terima kasih.", sample_answer="It works. Thank you.", focus="Result", expected_keywords=("works",)),
    ),
    "asking-for-opinions": (
        CoachTurn(coach="What do you think about going to Bali?", hint="Jawab dengan opini: I think it's + adjective.", sample_answer="I think it's a great idea.", focus="Give opinion", expected_keywords=("i think", "idea")),
        CoachTurn(coach="Why?", hint="Jawab dengan because + reason.", sample_answer="Because the beaches are beautiful.", focus="Give reason", expected_keywords=("because", "beaches")),
        CoachTurn(coach="Any concern?", hint="Sebutkan kekhawatiran: It might be ...", sample_answer="It might be crowded.", focus="Add concern politely", expected_keywords=("might", "crowded")),
    ),
    "asking-for-recommendations": (
        CoachTurn(coach="Hi. How can I help you today?", hint="Tanya rekomendasi buat dinner.", sample_answer="Do you have any recommendations for dinner?", focus="Ask for recommendations", expected_keywords=("recommendations",)),
        CoachTurn(coach="Sure. What kind of place are you looking for?", hint="Jelaskan yang kamu cari (local / quiet / cheap).", sample_answer="I'm looking for something local. Something local would be great.", focus="Describe what you want", expected_keywords=("looking for", "local")),
        CoachTurn(coach="I recommend a place nearby. Any questions?", hint="Tanya jarak atau cara pergi.", sample_answer="Great. Is it far from here?", focus="Ask a follow-up question", expected_keywords=("far", "here")),
    ),
    "asking-for-repetition": (
        CoachTurn(coach="My phone number is zero eight one three, two two five five.", hint="Minta lawan bicara mengulang.", sample_answer="Sorry, can you repeat that, please?", focus="Polite repetition", expected_keywords=("sorry", "repeat", "?")),
        CoachTurn(coach="Sure. Zero eight one three, two two five five.", hint="Cek satu detail dengan: Did you say ...?", sample_answer="Did you say two two five five?", focus="Checking a detail", expected_keywords=("did", "say", "two", "five", "?")),
        CoachTurn(coach="Yes, that's right.", hint="Tunjukkan bahwa kamu sudah paham.", sample_answer="Got it. Thank you.", focus="Showing understanding", expected_keywords=("got",)),
    ),
    "asking-high-quality-follow-ups": (
        CoachTurn(coach="Clarify what 'more cautious' means.", hint="When you say..., do you mean X or Y?", sample_answer="When you say 'more cautious', do you mean smaller scope or slower timing?", focus="Clarify", expected_keywords=("when you say", "do you mean")),
        CoachTurn(coach="Ask about assumptions and decision criteria.", hint="What's your assumption... What would change your mind...?", sample_answer="What's your assumption about the main risk? And what would change your mind about the timeline?", focus="Assumptions + criteria", expected_keywords=("assumption", "change your mind")),
        CoachTurn(coach="Move to action.", hint="What's the next step today?", sample_answer="Got it. What's the next step we should take today?", focus="Action", expected_keywords=("next step", "today")),
    ),
    "asking-how-to-get-there": (
        CoachTurn(coach="Where do you want to go?", hint="Tanyakan cara ke station.", sample_answer="How do I get to the station?", focus="Direction question", expected_keywords=("how", "get", "station", "?")),
        CoachTurn(coach="Go straight for two minutes.", hint="Ulangi durasi arahnya.", sample_answer="Okay. Go straight for two minutes.", focus="Time direction", expected_keywords=("straight", "two", "minutes")),
        CoachTurn(coach="Then turn right at the bank.", hint="Konfirmasi landmark.", sample_answer="Turn right at the bank?", focus="Landmark confirmation", expected_keywords=("turn", "right", "bank", "?")),
        CoachTurn(coach="Yes. The station is there.", hint="Tutup dengan sopan.", sample_answer="Thank you for your help.", focus="Thanking", expected_keywords=("help",)),
    ),
    "asking-someones-name": (
        CoachTurn(coach="Hi. I am new here.", hint="Tanyakan nama dengan: What's your name?", sample_answer="Hi. What's your name?", focus="Asking a name", expected_keywords=("what's your name", "what is your name", "may i know your name", "?"), indonesian_explanation="Tanyakan nama dengan pertanyaan sederhana. 'What's your name?' cukup untuk konteks santai."),
        CoachTurn(coach="My name is Mina.", hint="Ulangi nama orang itu dalam responsmu.", sample_answer="Nice to meet you, Mina.", focus="Using the name", expected_keywords=("nice to meet you", "mina"), indonesian_explanation="Mengulang nama lawan bicara membuat responsmu terdengar lebih perhatian."),
        CoachTurn(coach="Nice to meet you too.", hint="Tutup dengan respons singkat yang natural.", sample_answer="See you later.", focus="Closing", expected_keywords=("see you", "later", "bye"), indonesian_explanation="Gunakan closing sederhana seperti 'See you later' agar percakapan selesai dengan sopan."),
    ),
    "asking-tactful-questions": (
        CoachTurn(coach="Ask how they prefer to receive feedback.", hint="Would you mind if I ask...?", sample_answer="Would you mind if I ask how you prefer to receive feedback?", focus="Preference", expected_keywords=("would you mind", "prefer")),
        CoachTurn(coach="Clarify the format politely.", hint="If it's okay, could you clarify whether...?", sample_answer="If it's okay, could you clarify whether you'd prefer feedback in writing or in a call?", focus="Clarify", expected_keywords=("if it's okay", "clarify", "whether")),
        CoachTurn(coach="Check understanding about privacy.", hint="Just to make sure I understand...", sample_answer="Just to make sure I understand, should we share concerns privately first?", focus="Confirm", expected_keywords=("make sure", "privately")),
    ),
    "asking-when-something-happens": (
        CoachTurn(coach="When is the meeting?", hint="Jawab dengan hari dan jam.", sample_answer="It's tomorrow at ten.", focus="Event time", expected_keywords=("it's", "tomorrow", "ten")),
        CoachTurn(coach="Is it online?", hint="Jawab yes/no dengan kalimat lengkap.", sample_answer="Yes, it is online.", focus="Meeting format", expected_keywords=("online",)),
        CoachTurn(coach="Tomorrow at ten. Is that right?", hint="Konfirmasi dengan: Yes, that's right.", sample_answer="Yes, that's right.", focus="Confirming details", expected_keywords=("that's", "right")),
    ),
    "asking-where-a-place-is": (
        CoachTurn(coach="Excuse me. What do you need?", hint="Tanyakan lokasi classroom.", sample_answer="Where is the classroom?", focus="Place question", expected_keywords=("where", "classroom", "?")),
        CoachTurn(coach="It is on the first floor.", hint="Tanyakan apakah dekat office.", sample_answer="Is it near the office?", focus="Confirming location", expected_keywords=("near", "office", "?")),
        CoachTurn(coach="Yes, it is next to the office.", hint="Tutup dengan thank you.", sample_answer="Thank you.", focus="Polite closing", expected_keywords=()),
    ),
    "b1-final-conversation": (
        CoachTurn(coach="How was your practice last week?", hint="At first..., but then... because...", sample_answer="At first it was hard, but then it got easier because I kept sessions short.", focus="Story + reason", expected_keywords=("at first", "but", "because")),
        CoachTurn(coach="Nice. What's your goal now?", hint="My goal is to... by ...", sample_answer="My goal is to speak more confidently by next month.", focus="Goal with deadline", expected_keywords=("goal", "by")),
        CoachTurn(coach="What usually gets in your way, what helps you most, and what's your next step?", hint="Sometimes..., so... What helps me most is... My next step is...", sample_answer="Sometimes I get distracted, so I leave my phone in another room. I prefer Conversation Coach because it gives feedback. So my next step is to practice three times this week.", focus="Problem + preference + next step", expected_keywords=("so", "prefer", "because", "next step")),
    ),
    "b1-final-test-practice": (
        CoachTurn(coach="What's your goal this month?", hint="Goal + by ...", sample_answer="My goal is to speak more confidently by the end of this month.", focus="Goal with deadline", expected_keywords=("goal", "by")),
        CoachTurn(coach="What's your biggest challenge, and what will you do?", hint="Challenge + so ...", sample_answer="The biggest challenge is staying consistent, so I'm keeping sessions short.", focus="Challenge + solution", expected_keywords=("challenge", "so")),
        CoachTurn(coach="Compare and choose: option A or B?", hint="I prefer ... because ... but ...", sample_answer="I prefer option B because it's cheaper, but it might be crowded.", focus="Preference with reason + concern", expected_keywords=("prefer", "because", "might")),
    ),
    "b2-final-discussion": (
        CoachTurn(coach="Before we decide, can you define the scope and what success looks like?", hint="Let's define the scope... what does success look like?", sample_answer="We should keep the scope to the core workflow, and success means fewer incidents without delaying the release.", focus="Frame", expected_keywords=("scope", "success")),
        CoachTurn(coach="Leadership still wants new features, and I'm worried we'll overload the team.", hint="I understand the concern... The trade-off is...", sample_answer="I understand the concern. The trade-off is speed versus reliability, so we should keep scope tight.", focus="Concerns + trade-offs", expected_keywords=("understand", "trade-off")),
        CoachTurn(coach="Given all that, what do you recommend, and what are the next steps?", hint="Given these constraints... Next steps are... today... by Friday.", sample_answer="Given these constraints, I'd recommend a time-boxed pilot. Next steps are: I'll share a plan today, and you'll review it by Friday.", focus="Decision + next steps", expected_keywords=("recommend", "next steps", "by")),
    ),
    "b2-final-test-practice": (
        CoachTurn(coach="What's your position?", hint="My position is that...", sample_answer="My position is that we should run a two-week pilot before a full rollout.", focus="Position", expected_keywords=("position", "pilot")),
        CoachTurn(coach="What's your evidence and trade-off?", hint="Based on the data... The trade-off is...", sample_answer="Based on the data, drop-offs increased after the redesign. The trade-off is speed versus long-term reliability.", focus="Evidence + trade-off", expected_keywords=("based on", "data", "trade-off")),
        CoachTurn(coach="Recommend a next step and timeline.", hint="I'd recommend... Next steps are... by Friday.", sample_answer="I'd recommend the pilot. Next steps are: I'll draft the plan today, and you'll review it by Friday.", focus="Recommendation + next steps", expected_keywords=("recommend", "next steps", "by")),
    ),
    "balancing-two-viewpoints": (
        CoachTurn(coach="We need to choose between growth and stability.", hint="Mulai dengan on the one hand... on the other hand...", sample_answer="On the one hand, growth could unlock new revenue. On the other hand, stability reduces long-term risk.", focus="Balance", expected_keywords=("on the one hand", "on the other hand")),
        CoachTurn(coach="Give a nuanced conclusion.", hint="While it's true... On balance...", sample_answer="While it's true that growth matters, the incident rate is concerning. On balance, I'd prioritize stability.", focus="Conclusion", expected_keywords=("while it's true", "on balance")),
        CoachTurn(coach="Offer a compromise plan.", hint="Ring-fence a small budget...", sample_answer="I'd ring-fence a small budget for growth experiments while we focus on stability.", focus="Compromise", expected_keywords=("ring-fence", "budget")),
    ),
    "being-polite-with-differences": (
        CoachTurn(coach="In my country, people usually eat dinner early, around 6 p.m.", hint="Reaksi sopan + jelaskan kebiasaanmu.", sample_answer="Oh, that's interesting. In my country, we often eat later.", focus="Polite reaction + difference", expected_keywords=("interesting", "in my country")),
        CoachTurn(coach="Really? Are you used to eating early?", hint="Jawab dengan I'm not used to...", sample_answer="I'm not used to eating that early.", focus="Say unfamiliar politely", expected_keywords=("not used to",)),
        CoachTurn(coach="Say something respectful about my habit.", hint="Gunakan That sounds nice.", sample_answer="That sounds nice, especially if you sleep early.", focus="Show respect", expected_keywords=("sounds nice",)),
    ),
    "building-a-persuasive-flow": (
        CoachTurn(coach="What's the main argument for this proposal?", hint="Start with The core claim is...", sample_answer="The core claim is that modularization will improve delivery speed.", focus="Claim", expected_keywords=("core claim",)),
        CoachTurn(coach="What's the evidence?", hint="Use The evidence suggests...", sample_answer="The evidence suggests teams ship faster when ownership is clear.", focus="Evidence", expected_keywords=("evidence suggests",)),
        CoachTurn(coach="Address a concern and conclude.", hint="A common concern is... That said... In short...", sample_answer="A common concern is fragmentation. That said, shared standards can mitigate it. In short, the benefits outweigh the risks if we set guardrails early.", focus="Concern + conclusion", expected_keywords=("concern", "that said", "in short")),
    ),
    "buying-a-simple-item": (
        CoachTurn(coach="Hello. What do you need?", hint="Minta beli pen ini.", sample_answer="Can I have this pen?", focus="Buying item", expected_keywords=("have", "pen", "?")),
        CoachTurn(coach="Yes, of course.", hint="Tanyakan harganya.", sample_answer="How much is it?", focus="Price", expected_keywords=("how", "much", "?")),
        CoachTurn(coach="It is one dollar.", hint="Bayar dengan Here you go.", sample_answer="Okay. Here you go.", focus="Payment", expected_keywords=()),
        CoachTurn(coach="Thank you. Here is your pen.", hint="Tutup singkat.", sample_answer="Thanks.", focus="Closing", expected_keywords=()),
    ),
    "buying-a-ticket": (
        CoachTurn(coach="Hi. Where are you going?", hint="Sebutkan tujuan dan minta tiket dengan sopan.", sample_answer="I'd like one ticket to Bandung, please.", focus="Request a ticket", expected_keywords=("i'd like", "ticket")),
        CoachTurn(coach="One-way or round-trip?", hint="Pilih jenis tiket.", sample_answer="One-way, please.", focus="Choose the ticket type", expected_keywords=("one-way",)),
        CoachTurn(coach="Okay. That's 120,000 rupiah.", hint="Konfirmasi harga dengan pertanyaan singkat.", sample_answer="Okay. How much is it again?", focus="Confirm the price", expected_keywords=("how much", "?")),
    ),
    "c1-final-conversation": (
        CoachTurn(coach="Before we decide, what are we optimizing for here?", hint="Let me frame this...", sample_answer="Let me frame this: we need reliable outcomes and stakeholder confidence before scaling.", focus="Frame", expected_keywords=("frame", "confidence")),
        CoachTurn(coach="I agree, but some people still want to move faster, and no one wants to own a visible failure.", hint="On balance... What I'm hearing is... do you mean X or Y?", sample_answer="On balance, we can move fast, but only if we limit scope and validate metrics. What I'm hearing is some fear of visibility. Do you mean scope concerns or accountability concerns?", focus="Nuance + listening", expected_keywords=("on balance", "only if", "hearing")),
        CoachTurn(coach="Given that, what's your decision, and what should we do next?", hint="The decision is... Next steps are... today... tomorrow...", sample_answer="The decision is to run a two-week pilot with clear success criteria. Next steps are: I'll send a one-page plan today, and we'll align stakeholders tomorrow.", focus="Decision + next steps", expected_keywords=("decision", "next steps", "today")),
    ),
    "c1-final-test-practice": (
        CoachTurn(coach="Before we go further, what's the issue in one line?", hint="Let me frame this...", sample_answer="Let me frame this: we need reliability and stakeholder confidence before scaling.", focus="Frame", expected_keywords=("frame", "reliability")),
        CoachTurn(coach="Would you support the rollout now, or only under certain conditions?", hint="On balance... but only after...", sample_answer="On balance, I support the rollout, but only after we validate pilot metrics.", focus="Nuance", expected_keywords=("on balance", "only after", "validate")),
        CoachTurn(coach="Okay. So what's the decision, what are the open questions, and what should we do next?", hint="The decision is... The open questions are... Next steps are...", sample_answer="The decision is to run a two-week pilot. The open questions are resourcing and change management. Next steps are: I'll send a summary today, and we'll align tomorrow.", focus="Structure", expected_keywords=("decision", "open questions", "next steps")),
    ),
    "cafe-and-shop-mission": (
        CoachTurn(coach="Hi. What would you like?", hint="Pesan coffee dan sandwich.", sample_answer="Can I have a coffee and a sandwich, please?", focus="Mission order", expected_keywords=("have", "coffee", "sandwich", "?")),
        CoachTurn(coach="Sure. Small or large coffee?", hint="Pilih small.", sample_answer="Small, please.", focus="Size", expected_keywords=("small",)),
        CoachTurn(coach="Anything else?", hint="Tanyakan total harga.", sample_answer="How much is it?", focus="Total price", expected_keywords=("how", "much", "?")),
        CoachTurn(coach="It is five dollars.", hint="Bayar dengan sopan.", sample_answer="Okay. Here you go.", focus="Payment", expected_keywords=()),
        CoachTurn(coach="Thank you. Here is your order.", hint="Tutup singkat.", sample_answer="Thanks.", focus="Closing", expected_keywords=()),
    ),
    "catching-implied-meaning": (
        CoachTurn(coach="Interpret the concern neutrally.", hint="Use It sounds like...", sample_answer="It sounds like timing is the main concern.", focus="Interpretation", expected_keywords=("sounds like", "concern")),
        CoachTurn(coach="Confirm implied meaning politely.", hint="Just to check... are you implying...?", sample_answer="Just to check, are you implying that we should delay the rollout?", focus="Check", expected_keywords=("just to check", "implying", "delay")),
        CoachTurn(coach="Summarize and propose a next step.", hint="What I'm hearing is... I'll...", sample_answer="What I'm hearing is we need a phased plan to reduce risk. I'll draft a phased option and share it today.", focus="Next step", expected_keywords=("hearing", "phased", "share")),
    ),
    "challenging-an-argument": (
        CoachTurn(coach="Fewer steps always increases conversion.", hint="Challenge logic politely.", sample_answer="I'm not sure that follows. What's the evidence for that claim?", focus="Logic + evidence", expected_keywords=("not sure", "evidence")),
        CoachTurn(coach="I think it's common sense. What's your response?", hint="Introduce another explanation + example.", sample_answer="Could there be another explanation, like unclear copy or missing reassurance? For example, we reduced steps last quarter, but conversion didn't change.", focus="Alternatives", expected_keywords=("another explanation", "for example")),
        CoachTurn(coach="Close with a constructive next step.", hint="Let's test...", sample_answer="Let's test messaging changes alongside step reduction and compare results.", focus="Next step", expected_keywords=("test", "compare")),
    ),
    "checking-directions": (
        CoachTurn(coach="Go straight and turn left at the stairs.", hint="Ulangi arahan untuk memastikan.", sample_answer="Turn left at the stairs. Okay.", focus="Confirm directions", expected_keywords=("turn left", "stairs")),
        CoachTurn(coach="Yes. Platform 2 is on the left.", hint="Tanyakan konfirmasi singkat.", sample_answer="Great. Is this the right way?", focus="Check the way", expected_keywords=("right way", "?")),
        CoachTurn(coach="Yes, you're going the right way.", hint="Tutup dengan sopan.", sample_answer="Thank you.", focus="Close politely", expected_keywords=("thank",)),
    ),
    "checking-in": (
        CoachTurn(coach="Welcome. How can I help you?", hint="Mulai dengan: I'd like to check in.", sample_answer="Hi. I'd like to check in.", focus="Start check-in", expected_keywords=("check in",)),
        CoachTurn(coach="Sure. Do you have a reservation?", hint="Jawab dengan under + name.", sample_answer="Yes. I have a reservation under Faris Kim.", focus="Confirm reservation name", expected_keywords=("reservation", "under")),
        CoachTurn(coach="Great. Any questions about your stay?", hint="Tanya 1 hal (check-out / breakfast).", sample_answer="Yes. What time is check-out?", focus="Ask a practical question", expected_keywords=("what time", "check-out")),
    ),
    "clarifying-scope": (
        CoachTurn(coach="Ask what is in scope for this sprint.", hint="Gunakan Just to clarify...", sample_answer="Just to clarify, what exactly is in scope for this sprint?", focus="Ask scope", expected_keywords=("clarify", "in scope")),
        CoachTurn(coach="Ask if the admin dashboard is included.", hint="Gunakan Does this include...?", sample_answer="Does this include the admin dashboard changes?", focus="Ask inclusion", expected_keywords=("include", "admin")),
        CoachTurn(coach="Confirm what is out of scope and next step.", hint="Use out of scope + I'll update...", sample_answer="Got it. So that's out of scope for now. I'll update the ticket list.", focus="Confirm + next step", expected_keywords=("out of scope", "update")),
    ),
    "clear-argument-mission": (
        CoachTurn(coach="Do you think we should change our meeting format?", hint="Mulai dengan In my view...", sample_answer="In my view, we should move routine updates to a written summary.", focus="Position", expected_keywords=("in my view", "should")),
        CoachTurn(coach="Why do you think that?", hint="One reason is... Another reason is...", sample_answer="One reason is it saves time. Another reason is it improves focus.", focus="Reasons", expected_keywords=("one reason", "another reason")),
        CoachTurn(coach="I worry we'll lose useful discussion. How would you answer that, and what should we try next?", hint="For example... That's a fair point. However... Let's...", sample_answer="For example, last month we spent 30 minutes repeating updates. That's a fair point. However, we can keep one monthly live session. Let's run a one-month trial and review the results.", focus="Example + counterpoint + next steps", expected_keywords=("for example", "fair point", "however", "trial")),
    ),
    "client-conversation-mission": (
        CoachTurn(coach="We're onboarding a lot of new hires, and the current process is messy.", hint="Just to clarify... biggest pain point...", sample_answer="Just to clarify, who is the main user group and what's the biggest pain point today?", focus="Discovery", expected_keywords=("clarify", "pain point")),
        CoachTurn(coach="The biggest issue is delays, but we also need something reliable. What options do you recommend?", hint="We have two options... The trade-off is... I'd recommend...", sample_answer="We have two options: a quick fix this week, or a more robust solution in two weeks. The trade-off is speed versus stability. I'd recommend the robust option if the timeline allows.", focus="Options + recommendation", expected_keywords=("two options", "trade-off", "recommend")),
        CoachTurn(coach="I'm concerned about disruption during rollout. How would you reduce the risk, and what are the next steps?", hint="I understand the concern... To reduce the risk... Next steps are... Does that timeline work...?", sample_answer="I understand the concern. To reduce the risk, we can run a two-week pilot and send weekly summaries. Next steps are: I'll send a draft plan today, and you'll review it by Friday. Does that timeline work for you?", focus="Concerns + next steps", expected_keywords=("understand", "reduce", "next steps", "timeline")),
    ),
    "coaching-with-questions": (
        CoachTurn(coach="I'm stuck on how to handle this.", hint="Start with options.", sample_answer="Got it. What options do you see right now?", focus="Options", expected_keywords=("options",)),
        CoachTurn(coach="Now help define success.", hint="What would success look like...?", sample_answer="What would success look like for the pilot?", focus="Success", expected_keywords=("success look like",)),
        CoachTurn(coach="Unblock with a small next step and offer support.", hint="Smallest next step... support...", sample_answer="What's the smallest next step you can take today? And what support do you need from me?", focus="Next step + support", expected_keywords=("smallest", "next step", "support")),
    ),
    "communicating-risk": (
        CoachTurn(coach="What risks should we highlight to leadership?", hint="Start with The main risk is...", sample_answer="The main risk is a spike in incidents during rollout.", focus="Risk", expected_keywords=("main risk", "incidents")),
        CoachTurn(coach="How likely is that?", hint="There's a reasonable chance... given...", sample_answer="There's a reasonable chance, given recent instability.", focus="Likelihood", expected_keywords=("reasonable chance", "given")),
        CoachTurn(coach="Close with mitigation steps.", hint="We can mitigate it by... monitoring... rollback...", sample_answer="We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.", focus="Mitigation", expected_keywords=("mitigate", "monitoring", "rollback")),
    ),
    "community-culture-mission": (
        CoachTurn(coach="Tell me about your neighborhood.", hint="I live in... It's known for...", sample_answer="I live in a quiet neighborhood. It's known for food stalls and small parks.", focus="Describe community", expected_keywords=("neighborhood", "known for")),
        CoachTurn(coach="Share one local habit.", hint="People usually... especially on weekends.", sample_answer="People usually eat outside in the evening, especially on weekends.", focus="Share local habit", expected_keywords=("usually", "especially")),
        CoachTurn(coach="Now respond politely to a cultural difference.", hint="That's interesting. I'm not used to..., but it sounds nice.", sample_answer="Oh, that's interesting. I'm not used to that, but it sounds nice.", focus="Polite differences", expected_keywords=("interesting", "not used to", "sounds nice")),
    ),
    "comparing-simple-options": (
        CoachTurn(coach="This one is cheaper. It's 80,000 rupiah.", hint="Tanyakan opsi satunya.", sample_answer="And the other one?", focus="Ask about the other option", expected_keywords=("other one", "?")),
        CoachTurn(coach="The other one is 120,000 rupiah, but it's better quality.", hint="Pilih salah satu dengan singkat.", sample_answer="Okay. I'll take the cheaper one.", focus="Choose an option", expected_keywords=("i'll take", "cheaper")),
        CoachTurn(coach="Sure.", hint="Tutup dengan sopan.", sample_answer="Thank you.", focus="Close politely", expected_keywords=("thank",)),
    ),
    "comparing-two-options": (
        CoachTurn(coach="We have two options. What's the difference?", hint="Bandingin pakai but.", sample_answer="Option A is nicer, but it's more expensive.", focus="Compare options", expected_keywords=("but", "more")),
        CoachTurn(coach="Okay. And option B?", hint="Sebutkan 1-2 poin: cheaper/faster/crowded.", sample_answer="It's cheaper and faster, but it's usually crowded.", focus="Describe option B", expected_keywords=("cheaper", "faster")),
        CoachTurn(coach="Got it. Ask me what I prefer.", hint="Tanya: Which do you prefer?", sample_answer="Which do you prefer?", focus="Ask preference", expected_keywords=("prefer",)),
    ),
    "confirming-details": (
        CoachTurn(coach="Okay, you're booked for tomorrow at 3:30 p.m.", hint="Konfirmasi jamnya.", sample_answer="Let me confirm the time: 3:30 p.m., right?", focus="Confirm the time", expected_keywords=("confirm", "3:30", "right")),
        CoachTurn(coach="Yes, that's right.", hint="Sebutkan nama dan eja.", sample_answer="My name is Raka Park. P-A-R-K.", focus="Give name and spelling", expected_keywords=("my name is", "p-a-r-k")),
        CoachTurn(coach="Thank you. Do you have a phone number?", hint="Berikan nomor telepon.", sample_answer="Yes. It's 0812-345-678.", focus="Provide phone number", expected_keywords=("it's", "0812")),
    ),
    "confirming-next-steps": (
        CoachTurn(coach="Confirm the decision.", hint="To confirm, ...", sample_answer="To confirm, we'll start with a two-week pilot.", focus="Confirm decision", expected_keywords=("to confirm", "pilot")),
        CoachTurn(coach="List next steps with owners and deadlines.", hint="Next steps are: I'll... today, and you'll... by Friday.", sample_answer="Next steps are: I'll send the draft plan today, and you'll review it by Friday.", focus="Next steps", expected_keywords=("next steps", "by")),
        CoachTurn(coach="Check if the timeline works.", hint="Does that timeline work for you?", sample_answer="Great. Does that timeline work for you?", focus="Confirm timeline", expected_keywords=("timeline", "work")),
    ),
    "contact-details-mission": (
        CoachTurn(coach="Hi. I need your contact details.", hint="Mulai dengan nama lengkapmu.", sample_answer="Sure. My name is Dimas.", focus="Sharing a name", expected_keywords=("sure", "name", "dimas")),
        CoachTurn(coach="How do you spell your name?", hint="Eja nama huruf demi huruf.", sample_answer="D-I-M-A-S.", focus="Spelling a name", expected_keywords=()),
        CoachTurn(coach="What is your phone number?", hint="Sebutkan nomor telepon dalam kelompok kecil.", sample_answer="It's zero eight one two, three four five six.", focus="Sharing a phone number", expected_keywords=("it's", "zero", "eight", "one")),
        CoachTurn(coach="And your email address?", hint="Sebutkan email dengan at dan dot.", sample_answer="It's dimas at example dot com.", focus="Sharing an email", expected_keywords=("it's", "dimas", "example", "dot")),
        CoachTurn(coach="Is everything correct?", hint="Konfirmasi semua informasi benar.", sample_answer="Yes, everything is correct.", focus="Confirming all details", expected_keywords=("everything", "correct")),
    ),
    "cross-cultural-mission": (
        CoachTurn(coach="They sounded polite, but I think they were uncomfortable. How do you read that?", hint="My sense is that... Before we decide, can we clarify...?", sample_answer="My sense is that they're signaling concern indirectly. Before we decide, can we clarify whether they prioritize speed or risk reduction?", focus="Context", expected_keywords=("my sense", "clarify", "priority")),
        CoachTurn(coach="That makes sense. How would you ask about feedback preferences tactfully?", hint="Would you mind if I ask...?", sample_answer="Would you mind if I ask how you prefer to receive feedback—writing or a call?", focus="Tactful question", expected_keywords=("would you mind", "prefer")),
        CoachTurn(coach="I may have come across too directly. How would you repair that and suggest a next step?", hint="I may have misunderstood... Just to clarify... How about we...?", sample_answer="I may have misunderstood their tone. Just to clarify, my intent was to confirm constraints, not reject the request. How about we send a short note and offer a quick call?", focus="Repair", expected_keywords=("misunderstood", "intent", "how about")),
    ),
    "days-and-simple-schedules": (
        CoachTurn(coach="When is the English class?", hint="Jawab dengan hari: on Monday and Wednesday.", sample_answer="It's on Monday and Wednesday.", focus="Class days", expected_keywords=("it's", "monday", "wednesday")),
        CoachTurn(coach="What time?", hint="Jawab dengan at + time.", sample_answer="At seven in the evening.", focus="Class time", expected_keywords=("seven", "evening")),
        CoachTurn(coach="Great. See you on Monday.", hint="Tutup dengan singkat.", sample_answer="See you.", focus="Schedule closing", expected_keywords=("see",)),
    ),
    "debate-analysis-mission": (
        CoachTurn(coach="Challenge the claim by surfacing an assumption and asking for evidence.", hint="It seems you're assuming... What's the evidence for...?", sample_answer="It seems you're assuming fewer steps automatically mean better conversion. What's the evidence for that claim?", focus="Assumption + evidence", expected_keywords=("assuming", "evidence")),
        CoachTurn(coach="Present evidence carefully and be precise about what it shows.", hint="According to... To be precise...", sample_answer="According to the support dashboard, drop-offs increased after the redesign. To be precise, the data indicates correlation, not necessarily causation.", focus="Evidence + precision", expected_keywords=("according to", "precise", "correlation")),
        CoachTurn(coach="Respond under pressure and propose a controlled next step.", hint="Let me be clear... key point... pilot...", sample_answer="Let me be clear: we have indicators, not proof yet. However, the key point is waiting increases risk. We run a pilot this week and review results before scaling.", focus="Pressure response", expected_keywords=("be clear", "key point", "pilot")),
    ),
    "describing-a-problem": (
        CoachTurn(coach="What's going on?", hint="Mulai dengan: There's a problem with ...", sample_answer="There's a problem with the login page.", focus="State the problem", expected_keywords=("problem", "with")),
        CoachTurn(coach="When did it start?", hint="Jawab kapan mulai.", sample_answer="It started this morning when we deployed the update.", focus="State timing and trigger", expected_keywords=("started", "when")),
        CoachTurn(coach="What is the impact?", hint="Jelaskan dampak pakai so.", sample_answer="Users can't sign in, so they can't access their lessons.", focus="Explain impact", expected_keywords=("can't", "so")),
    ),
    "describing-a-simple-experience": (
        CoachTurn(coach="Oh nice. How was it?", hint="Jawab dengan It was + adjective.", sample_answer="It was delicious.", focus="Describe with adjective", expected_keywords=("it was",)),
        CoachTurn(coach="What did you eat?", hint="Sebutkan makanan (past).", sample_answer="I ate grilled chicken and salad.", focus="Say what you ate", expected_keywords=("ate",)),
        CoachTurn(coach="Would you go again?", hint="Jawab dan bilang kamu suka / tidak suka.", sample_answer="Yes. I really liked it.", focus="Give opinion", expected_keywords=("liked",)),
    ),
    "describing-feelings": (
        CoachTurn(coach="How did you feel when that happened?", hint="Sebutkan perasaan + sebab singkat.", sample_answer="I felt nervous because we got lost.", focus="Describe feeling with reason", expected_keywords=("felt", "because")),
        CoachTurn(coach="What did you do next?", hint="Sebutkan solusi singkat.", sample_answer="We asked for directions.", focus="Describe an action", expected_keywords=("asked",)),
        CoachTurn(coach="And how did you feel after that?", hint="Sebutkan perasaan setelahnya.", sample_answer="I felt relieved after that.", focus="Describe feeling after", expected_keywords=("relieved",)),
    ),
    "describing-simple-symptoms": (
        CoachTurn(coach="What seems to be the problem?", hint="Sebutkan gejala + durasi.", sample_answer="I've had a sore throat since yesterday.", focus="Describe symptom with duration", expected_keywords=("have had", "since", "throat")),
        CoachTurn(coach="Do you have a fever?", hint="Jawab singkat, lalu tambah gejala.", sample_answer="A little. And I have a cough.", focus="Add another symptom", expected_keywords=("a little", "cough")),
        CoachTurn(coach="How long have you been coughing?", hint="Jawab durasinya.", sample_answer="For two days.", focus="State duration", expected_keywords=("for", "days")),
    ),
    "describing-your-community": (
        CoachTurn(coach="What's your neighborhood like?", hint="Mulai dengan I live in ... neighborhood.", sample_answer="I live in a quiet neighborhood near the city center.", focus="Describe neighborhood", expected_keywords=("neighborhood",)),
        CoachTurn(coach="What is it known for?", hint="Jawab dengan It's known for ...", sample_answer="It's known for its food stalls and small parks.", focus="Say what it's known for", expected_keywords=("known for",)),
        CoachTurn(coach="What do you like about it?", hint="Jawab dengan because + reason.", sample_answer="I like it because it's convenient but still peaceful.", focus="Give a reason", expected_keywords=("because", "convenient")),
    ),
    "discussing-challenges": (
        CoachTurn(coach="What's the biggest challenge?", hint="Jawab dengan The biggest challenge is ...", sample_answer="The biggest challenge is staying consistent after work.", focus="Name the challenge", expected_keywords=("challenge", "consistent")),
        CoachTurn(coach="Why is it hard?", hint="Sebutkan satu alasan (distracted/tired).", sample_answer="I get distracted by my phone, and I feel tired.", focus="Explain the reason", expected_keywords=("distracted", "tired")),
        CoachTurn(coach="Okay. What do you want to ask me?", hint="Minta saran singkat.", sample_answer="Do you have any tips?", focus="Ask for a suggestion", expected_keywords=("tips",)),
    ),
    "discussing-reliable-sources": (
        CoachTurn(coach="Is this source reliable?", hint="I'm not sure it's reliable.", sample_answer="I'm not sure that source is reliable.", focus="Express doubt", expected_keywords=("not sure", "reliable")),
        CoachTurn(coach="Why not?", hint="Because it doesn't cite... / mention...", sample_answer="Because it doesn't cite data or mention the author.", focus="Give criteria", expected_keywords=("doesn't", "cite")),
        CoachTurn(coach="What would you do next?", hint="I'd check ...", sample_answer="I'd check official reports or reputable news outlets before sharing.", focus="Suggest verification", expected_keywords=("I'd check", "official")),
    ),
    "discussing-tradeoffs": (
        CoachTurn(coach="We have two options. Compare them.", hint="Mulai dengan trade-off.", sample_answer="The trade-off is speed versus long-term reliability.", focus="Trade-off", expected_keywords=("trade-off",)),
        CoachTurn(coach="Explain the downside of the fast option.", hint="If we optimize for speed, we might...", sample_answer="If we optimize for speed, we might introduce more bugs.", focus="Impact", expected_keywords=("optimize", "might")),
        CoachTurn(coach="Now contrast with the safer option.", hint="On the other hand...", sample_answer="On the other hand, the slower option reduces risk but takes more effort.", focus="Contrast", expected_keywords=("on the other hand", "risk")),
    ),
    "explaining-a-delay": (
        CoachTurn(coach="Hi. Are you on your way?", hint="Jawab + bilang kamu telat.", sample_answer="Yes, but I'm running a bit late.", focus="State you are late", expected_keywords=("running", "late")),
        CoachTurn(coach="What happened?", hint="Sebutkan transport kamu delayed.", sample_answer="My train is delayed because of a signal problem.", focus="Give a reason", expected_keywords=("delayed", "because")),
        CoachTurn(coach="When will you arrive?", hint="Kasih estimasi in about + time.", sample_answer="I'll be there in about 20 minutes.", focus="Give an estimate", expected_keywords=("in about", "minutes")),
    ),
    "explaining-a-viewpoint": (
        CoachTurn(coach="What's your take on this?", hint="From my perspective, ...", sample_answer="From my perspective, some regulation is necessary.", focus="Viewpoint", expected_keywords=("from my perspective",)),
        CoachTurn(coach="Why?", hint="The reason is ...", sample_answer="The reason is it protects users from misuse and misinformation.", focus="Reason", expected_keywords=("the reason is",)),
        CoachTurn(coach="I disagree. It could slow innovation.", hint="Acknowledge: I see the other side, but...", sample_answer="I see the other side, but basic safety rules can still support innovation.", focus="Acknowledge + respond", expected_keywords=("other side", "but")),
    ),
    "explaining-benefits-and-risks": (
        CoachTurn(coach="What is the main benefit?", hint="The main benefit is ...", sample_answer="The main benefit is faster onboarding for new hires.", focus="Benefit 1", expected_keywords=("main benefit",)),
        CoachTurn(coach="Give another benefit.", hint="Another benefit is ...", sample_answer="Another benefit is fewer repeated questions for the team.", focus="Benefit 2", expected_keywords=("another benefit",)),
        CoachTurn(coach="Now mention a key risk and mitigation.", hint="A key risk is... To reduce the risk, we can...", sample_answer="A key risk is that it becomes outdated. To reduce the risk, we can review it monthly and assign an owner.", focus="Risk + mitigation", expected_keywords=("risk", "reduce")),
    ),
    "explaining-causes": (
        CoachTurn(coach="Why do you think this problem is happening?", hint="Jawab dengan one possible cause is...", sample_answer="One possible cause is the new checkout design.", focus="Possible cause", expected_keywords=("possible cause",)),
        CoachTurn(coach="What evidence do we have?", hint="Pakai based on the data.", sample_answer="Based on the data, drop-offs increased right after the redesign.", focus="Evidence", expected_keywords=("based on", "data")),
        CoachTurn(coach="How can we confirm this?", hint="Usulkan test/compare.", sample_answer="Let's compare load times and run a small A/B test.", focus="Confirm", expected_keywords=("compare", "test")),
    ),
    "explaining-local-norms": (
        CoachTurn(coach="Explain a local norm about disagreement.", hint="In our context... people tend to...", sample_answer="In our context, people tend to be indirect when disagreeing in group settings.", focus="Norm", expected_keywords=("context", "tend to", "indirect")),
        CoachTurn(coach="Explain what's generally expected.", hint="It's generally expected that...", sample_answer="It's generally expected that you raise concerns one-on-one first.", focus="Expectation", expected_keywords=("generally expected", "one-on-one")),
        CoachTurn(coach="Offer a practical tip.", hint="It might help to...", sample_answer="It might help to start with appreciation, then ask a question instead of stating a critique.", focus="Tip", expected_keywords=("might help", "appreciation", "question")),
    ),
    "explaining-options": (
        CoachTurn(coach="Can you explain our options?", hint="Mulai dengan We have two options.", sample_answer="We have two options. Option A is a quick fix we can deliver this week.", focus="Option A", expected_keywords=("two options", "option a")),
        CoachTurn(coach="And option B?", hint="Option B is..., but it takes...", sample_answer="Option B is a more robust solution, but it takes two more weeks.", focus="Option B", expected_keywords=("option b", "but")),
        CoachTurn(coach="Explain the trade-off and recommend one.", hint="The trade-off is... I'd recommend...", sample_answer="The trade-off is speed versus long-term stability. I'd recommend option B if the timeline allows.", focus="Trade-off + recommendation", expected_keywords=("trade-off", "recommend")),
    ),
    "explaining-progress": (
        CoachTurn(coach="How's your goal going?", hint="Mulai dengan: I'm making good progress.", sample_answer="I'm making good progress.", focus="Share progress", expected_keywords=("progress",)),
        CoachTurn(coach="What have you been doing?", hint="Jawab dengan I've been practicing ...", sample_answer="I've been practicing every morning for five minutes.", focus="Explain practice habit", expected_keywords=("been", "practicing")),
        CoachTurn(coach="What still needs work?", hint="Jawab dengan I still need to ...", sample_answer="I still need to improve my pronunciation.", focus="State what's next to improve", expected_keywords=("still", "improve")),
    ),
    "explaining-why-you-prefer-something": (
        CoachTurn(coach="Which one do you prefer?", hint="Jawab dengan I prefer ...", sample_answer="I prefer the earlier flight.", focus="State preference", expected_keywords=("prefer",)),
        CoachTurn(coach="Why?", hint="Jawab dengan because + reason.", sample_answer="Because it gives us more time in the afternoon.", focus="Explain reason", expected_keywords=("because", "time")),
        CoachTurn(coach="What is the main reason?", hint="Gunakan The main reason is ...", sample_answer="The main reason is I don't want to arrive too late.", focus="State main reason", expected_keywords=("main reason", "don't want")),
    ),
    "explaining-your-task": (
        CoachTurn(coach="Hi. What are you working on today?", hint="Jelaskan task kamu: I'm working on ...", sample_answer="I'm working on the onboarding email flow.", focus="State current task", expected_keywords=("working on",)),
        CoachTurn(coach="Great. What's the next step?", hint="Gunakan Next, I'll ...", sample_answer="Next, I'll review the copy and update the templates.", focus="State next step", expected_keywords=("next", "review")),
        CoachTurn(coach="Any blockers?", hint="Jawab singkat (none / one blocker).", sample_answer="Not right now, but I may need feedback later.", focus="Mention blockers", expected_keywords=("not", "feedback")),
    ),
    "expressing-certainty-and-doubt": (
        CoachTurn(coach="Will this change work as expected?", hint="Jawab dengan I'm fairly confident... given...", sample_answer="I'm fairly confident it will, given the support trends.", focus="Confidence", expected_keywords=("fairly confident", "given")),
        CoachTurn(coach="So we can roll it out broadly?", hint="I'm not entirely convinced... strong chance...", sample_answer="I'm not entirely convinced. There's a strong chance we'll see edge cases.", focus="Doubt", expected_keywords=("not entirely convinced", "strong chance")),
        CoachTurn(coach="Close with a safe plan.", hint="Limited rollout + metrics.", sample_answer="Let's start with a limited rollout and define clear success metrics.", focus="Plan", expected_keywords=("limited rollout", "metrics")),
    ),
    "expressing-priorities": (
        CoachTurn(coach="What's your top priority?", hint="Mulai dengan My top priority is...", sample_answer="My top priority is shipping the core feature safely.", focus="State top priority", expected_keywords=("top priority", "is")),
        CoachTurn(coach="Why is that important?", hint="Jawab dengan because + reason.", sample_answer="Because it's the main value for users and the deadline is close.", focus="Give reason", expected_keywords=("because", "deadline")),
        CoachTurn(coach="Ask about my priorities.", hint="Gunakan What about you? What's your top priority?", sample_answer="What about you? What's your top priority?", focus="Ask other priorities", expected_keywords=("what about you", "top priority")),
    ),
    "final-test-practice": (
        CoachTurn(coach="Hello. What is your name?", hint="Jawab dengan nama lengkap atau nama panggilan.", sample_answer="My name is Alya.", focus="Test identity", expected_keywords=("name", "alya")),
        CoachTurn(coach="Where are you from?", hint="Jawab asal dengan I'm from ...", sample_answer="I'm from Indonesia.", focus="Test origin", expected_keywords=("i'm", "from", "indonesia")),
        CoachTurn(coach="What do you do every morning?", hint="Sebutkan rutinitas belajar dan jam.", sample_answer="I study English at seven.", focus="Test routine", expected_keywords=("study", "english", "seven")),
        CoachTurn(coach="When is your class?", hint="Kalau perlu, minta pengulangan dulu.", sample_answer="Sorry, can you repeat that, please?", focus="Clarification", expected_keywords=("sorry", "repeat", "?")),
        CoachTurn(coach="Sure. When is your class?", hint="Jawab hari dan jam.", sample_answer="It is on Tuesday at eight.", focus="Schedule answer", expected_keywords=("tuesday", "eight")),
    ),
    "finding-a-place-mission": (
        CoachTurn(coach="Hello. Can I help you?", hint="Mulai sopan dan tanya cara ke room A.", sample_answer="Excuse me. How do I get to room A?", focus="Mission opening", expected_keywords=("excuse", "how", "get", "room", "?")),
        CoachTurn(coach="Go straight and turn left.", hint="Ulangi arahan lengkap.", sample_answer="Go straight and turn left.", focus="Combined directions", expected_keywords=("straight", "turn", "left")),
        CoachTurn(coach="Room A is next to the office.", hint="Konfirmasi lantai.", sample_answer="Is it on the first floor?", focus="Floor confirmation", expected_keywords=("first", "floor", "?")),
        CoachTurn(coach="Yes, it is.", hint="Tutup dengan thank you.", sample_answer="Great. Thank you.", focus="Closing", expected_keywords=("great",)),
    ),
    "finding-middle-ground": (
        CoachTurn(coach="We disagree. How can we move forward?", hint="Mulai dengan Maybe we can find a compromise.", sample_answer="Maybe we can find a compromise.", focus="Suggest compromise", expected_keywords=("compromise",)),
        CoachTurn(coach="Propose a middle-ground option.", hint="A compromise could be...", sample_answer="A compromise could be launching to 10% of users first.", focus="Propose middle ground", expected_keywords=("could be", "users")),
        CoachTurn(coach="Ask for agreement with a condition.", hint="If we do X, can we agree on Y?", sample_answer="If we do a small rollout, can we agree on one extra day for testing?", focus="Confirm agreement", expected_keywords=("if", "agree")),
    ),
    "first-conversation-mission": (
        CoachTurn(coach="Hi, good morning. My name is Sara.", hint="Sapa balik dan sebutkan namamu.", sample_answer="Good morning. My name is Arif.", focus="Greeting and name", expected_keywords=("good morning", "my name is", "i'm", "i am"), indonesian_explanation="Gabungkan greeting dan nama dalam dua kalimat pendek agar pembuka percakapan terasa jelas."),
        CoachTurn(coach="Nice to meet you. Where are you from?", hint="Jawab asalmu lalu tanyakan balik.", sample_answer="I'm from Indonesia. How about you?", focus="Origin and follow-up", expected_keywords=("from", "indonesia", "how about you", "?"), indonesian_explanation="Setelah menjawab asal, tanyakan balik supaya percakapan tidak berhenti."),
        CoachTurn(coach="I'm from Malaysia. Nice to meet you.", hint="Balas dan tutup percakapan.", sample_answer="Nice to meet you too. See you later.", focus="Closing mission", expected_keywords=("nice to meet you too", "see you", "later"), indonesian_explanation="Tutup misi dengan respons sopan dan closing singkat seperti 'See you later'."),
    ),
    "framing-a-complex-topic": (
        CoachTurn(coach="Can you present the proposal?", hint="Start with Today I'd like to...", sample_answer="Sure. Today I'd like to walk you through the proposal and why it matters.", focus="Opener", expected_keywords=("today", "walk you through", "matters")),
        CoachTurn(coach="Define the key term clearly.", hint="By X, I mean...", sample_answer="By 'modular architecture', I mean we separate features into independent components.", focus="Definition", expected_keywords=("by", "i mean", "independent")),
        CoachTurn(coach="State the purpose and preview the structure.", hint="The purpose of this is... First, I'll...", sample_answer="The purpose of this is to reduce coupling and speed up delivery. First, I'll outline the problem, then the proposed approach.", focus="Purpose + structure", expected_keywords=("purpose", "first", "then")),
    ),
    "framing-the-problem": (
        CoachTurn(coach="We have a complex issue to solve.", hint="Mulai dengan ajak tim framing dulu.", sample_answer="Got it. Let's define the problem statement first.", focus="Frame first", expected_keywords=("define", "problem")),
        CoachTurn(coach="Okay. What should we clarify first?", hint="Tanya scope.", sample_answer="Can we agree on the scope? Which area is affected?", focus="Scope", expected_keywords=("scope", "affected")),
        CoachTurn(coach="How do we know we succeeded?", hint="Tanya success criteria.", sample_answer="What does success look like for the next four weeks?", focus="Success criteria", expected_keywords=("success", "look like")),
    ),
    "giving-a-short-update": (
        CoachTurn(coach="Quick update: how is it going?", hint="Jawab dengan progress.", sample_answer="I'm making good progress. I'm almost done with the summary.", focus="Share progress", expected_keywords=("progress", "almost")),
        CoachTurn(coach="Great. What's left?", hint="Sebutkan 1-2 item yang tersisa.", sample_answer="I still need to update the risk section and double-check the numbers.", focus="Say what's left", expected_keywords=("still need", "double-check")),
        CoachTurn(coach="Any concerns?", hint="Sebutkan 1 concern dengan might need.", sample_answer="One concern is time. I might need an extra hour to review everything.", focus="Mention a concern", expected_keywords=("concern", "might")),
    ),
    "giving-actionable-feedback": (
        CoachTurn(coach="Give one suggestion, starting with a positive frame.", hint="Overall it's... One thing I'd suggest is...", sample_answer="Overall it's solid. One thing I'd suggest is leading with the decision.", focus="Suggestion", expected_keywords=("overall", "one thing")),
        CoachTurn(coach="Explain the impact.", hint="The impact is that...", sample_answer="The impact is that stakeholders scan quickly and might miss the point.", focus="Impact", expected_keywords=("impact", "might miss")),
        CoachTurn(coach="Propose a concrete improvement and invite revision.", hint="A concrete improvement would be... Would you be open to...?", sample_answer="A concrete improvement would be a one-line summary at the top. Would you be open to revising it and sending a second draft?", focus="Improve + invite", expected_keywords=("concrete", "open to")),
    ),
    "giving-constructive-feedback": (
        CoachTurn(coach="Any feedback on my demo?", hint="Mulai positif + I noticed...", sample_answer="Overall it was clear. I noticed the introduction was a bit long.", focus="Positive + observation", expected_keywords=("overall", "noticed")),
        CoachTurn(coach="What was the impact?", hint="Jelaskan impact dengan so.", sample_answer="Some people lost focus, so the key message came late.", focus="Explain impact", expected_keywords=("so", "message")),
        CoachTurn(coach="What would you suggest?", hint="Gunakan One suggestion is... / It might help if...", sample_answer="One suggestion is to start with the main takeaway. It might help if you keep the intro under one minute.", focus="Give a suggestion", expected_keywords=("suggestion", "might help")),
    ),
    "giving-phone-numbers": (
        CoachTurn(coach="What is your phone number?", hint="Sebutkan nomor telepon dalam kelompok kecil.", sample_answer="It's zero eight one two, three four five six.", focus="Giving a phone number", expected_keywords=("it's", "zero", "eight", "one")),
        CoachTurn(coach="Let me check. Zero eight one two, three four five six?", hint="Konfirmasi dengan: Yes, that's correct.", sample_answer="Yes, that's correct.", focus="Confirming a number", expected_keywords=("that's", "correct")),
        CoachTurn(coach="My number is zero eight one three, two two five five.", hint="Minta diulang dengan sopan.", sample_answer="Can you repeat that, please?", focus="Asking for repetition", expected_keywords=("repeat", "?")),
    ),
    "giving-simple-reasons": (
        CoachTurn(coach="Do you like this cafe?", hint="Jawab yes/no + opini singkat.", sample_answer="Yes, I like it.", focus="Give an opinion", expected_keywords=("yes", "like")),
        CoachTurn(coach="Why?", hint="Jawab dengan because + reason.", sample_answer="Because the coffee is good.", focus="Give a reason", expected_keywords=("because", "good")),
        CoachTurn(coach="What else do you like about it?", hint="Tambahkan satu alasan lain.", sample_answer="Because it is quiet and relaxing.", focus="Add another reason", expected_keywords=("because", "quiet")),
    ),
    "goals-progress-mission": (
        CoachTurn(coach="What's your goal right now?", hint="Goal + deadline (by ...).", sample_answer="My goal is to speak more confidently by the end of this month.", focus="Goal with deadline", expected_keywords=("goal", "by")),
        CoachTurn(coach="How's it going?", hint="Progress + I've been practicing ...", sample_answer="I'm making progress. I've been practicing every morning.", focus="Progress update", expected_keywords=("progress", "been")),
        CoachTurn(coach="Any challenges and next steps?", hint="Challenge + next step plan.", sample_answer="The biggest challenge is staying consistent after work. My next step is to practice three times this week.", focus="Challenge and next step", expected_keywords=("challenge", "next step", "times")),
    ),
    "guiding-a-decision": (
        CoachTurn(coach="Structure the options.", hint="We have three options...", sample_answer="We have three options: pilot, phased rollout, or full rollout.", focus="Options", expected_keywords=("options",)),
        CoachTurn(coach="Explain the trade-off and recommend an option.", hint="The trade-off is... Given our constraints, I'd recommend...", sample_answer="The trade-off is speed versus risk and operational load. Given our constraints, I'd recommend a phased rollout with clear monitoring.", focus="Trade-off + recommend", expected_keywords=("trade-off", "constraints", "recommend")),
        CoachTurn(coach="Confirm agreement on next steps.", hint="Can we agree on... review weekly...", sample_answer="Can we agree on the scope today and review metrics weekly?", focus="Agreement", expected_keywords=("agree", "scope", "weekly")),
    ),
    "handling-a-simple-complaint": (
        CoachTurn(coach="Hi. How can I help you?", hint="Mulai dengan: There's a problem with ...", sample_answer="Hi. There's a problem with my room.", focus="Start complaint politely", expected_keywords=("problem", "room")),
        CoachTurn(coach="I'm sorry to hear that. What's wrong?", hint="Jelaskan masalahnya (isn't working).", sample_answer="The air conditioning isn't working.", focus="Explain the issue", expected_keywords=("isn't working",)),
        CoachTurn(coach="Okay. What would you like us to do?", hint="Minta bantuan (Could you...) atau opsi (Could I...).", sample_answer="Could you send someone to take a look? Could I change rooms if it can't be fixed?", focus="Request help or alternative", expected_keywords=("could", "send", "change")),
    ),
    "handling-challenging-questions": (
        CoachTurn(coach="Isn't this approach too risky?", hint="That's a fair question... Let me clarify...", sample_answer="That's a fair question. Let me clarify what risk we're accepting.", focus="Acknowledge", expected_keywords=("fair question", "clarify")),
        CoachTurn(coach="Give the short answer and condition.", hint="The short answer is...", sample_answer="The short answer is: it's manageable if we pilot first and monitor closely.", focus="Short answer", expected_keywords=("short answer", "manageable", "pilot")),
        CoachTurn(coach="Close with emphasis and a fallback plan.", hint="What I'd emphasize... If adoption stalls...", sample_answer="What I'd emphasize is that standards need ownership and enforcement. If adoption stalls, we pause expansion and revisit the design.", focus="Emphasis + fallback", expected_keywords=("emphasize", "ownership", "pause")),
    ),
    "handling-concerns": (
        CoachTurn(coach="I'm concerned this change will disrupt our team.", hint="Mulai dengan I understand the concern.", sample_answer="I understand the concern.", focus="Acknowledge", expected_keywords=("understand", "concern")),
        CoachTurn(coach="Ask me what I mean.", hint="Could you clarify...?", sample_answer="Could you clarify what disruption you expect?", focus="Clarify", expected_keywords=("clarify",)),
        CoachTurn(coach="Offer a mitigation plan.", hint="To reduce the risk, we can...", sample_answer="To reduce the risk, we can run a two-week trial, send weekly summaries, and gather feedback.", focus="Mitigation", expected_keywords=("reduce", "trial", "feedback")),
    ),
    "handling-objections": (
        CoachTurn(coach="I'm concerned this plan will slow us down.", hint="Mulai dengan I understand the concern.", sample_answer="I understand the concern.", focus="Acknowledge", expected_keywords=("understand", "concern")),
        CoachTurn(coach="Ask me what part feels risky.", hint="Gunakan What part feels risky to you?", sample_answer="What part feels risky to you?", focus="Clarify", expected_keywords=("risky",)),
        CoachTurn(coach="Offer a revised proposal.", hint="Would it help if... / What if we...", sample_answer="Would it help if we limit reviews to high-risk changes only? What if we define simple criteria together?", focus="Revise proposal", expected_keywords=("would it help", "what if")),
    ),
    "handling-sensitive-feedback": (
        CoachTurn(coach="How did the last review go?", hint="Mulai dengan I wanted to flag...", sample_answer="It went well overall. I wanted to flag one point about the messaging.", focus="Opener", expected_keywords=("flag", "messaging")),
        CoachTurn(coach="What was the issue?", hint="Fokus ke impact.", sample_answer="The impact is that some teams interpreted it as a hard deadline.", focus="Impact", expected_keywords=("impact", "interpreted", "deadline")),
        CoachTurn(coach="Suggest a fix politely.", hint="Would you be open to...?", sample_answer="Would you be open to adding an explicit 'earliest possible' line to clarify the timeline?", focus="Suggestion", expected_keywords=("open to", "explicit", "clarify")),
    ),
    "health-appointment-mission": (
        CoachTurn(coach="Hello. How can I help you today?", hint="Bilang kamu ada janji + jamnya.", sample_answer="Hi. I have an appointment at 3:30.", focus="Check in for appointment", expected_keywords=("appointment", "3:30")),
        CoachTurn(coach="Sure. What's your name?", hint="Sebutkan nama dan eja.", sample_answer="Raka Park. P-A-R-K.", focus="Provide name and spelling", expected_keywords=("p-a-r-k", "raka")),
        CoachTurn(coach="Thank you. What seems to be the problem?", hint="Sebutkan gejala + durasi.", sample_answer="I've had a cough for two days, and I feel tired.", focus="Describe symptoms with duration", expected_keywords=("have had", "for", "days", "tired")),
    ),
    "help-and-problem-mission": (
        CoachTurn(coach="Hi. Is everything okay?", hint="Katakan kamu tidak mengerti.", sample_answer="Sorry, I don't understand.", focus="Mission opening", expected_keywords=("sorry", "don't", "understand")),
        CoachTurn(coach="That's okay. What is the problem?", hint="Jelaskan masalah file.", sample_answer="I can't open this file.", focus="Problem", expected_keywords=("can't", "open", "file")),
        CoachTurn(coach="Can you send me a screenshot?", hint="Terima dan minta tunggu sebentar.", sample_answer="Sure. Can you wait a minute?", focus="Request", expected_keywords=("sure", "wait", "minute", "?")),
        CoachTurn(coach="No problem.", hint="Kirim screenshot.", sample_answer="Here is the screenshot.", focus="Sending info", expected_keywords=("screenshot",)),
        CoachTurn(coach="Good. Click this button.", hint="Katakan berhasil dan terima kasih.", sample_answer="It works. Thank you for your help.", focus="Closing", expected_keywords=("works", "help")),
    ),
    "idea-presentation-mission": (
        CoachTurn(coach="Present your idea in 2-3 sentences with signposting.", hint="Today I'd like to... First... Next... Finally...", sample_answer="Today I'd like to propose a shared onboarding checklist. First, the problem is inconsistency. Next, the proposal is a checklist plus a buddy. Finally, we'll pilot it next week.", focus="Presentation with signposting", expected_keywords=("today", "first", "next", "finally")),
        CoachTurn(coach="Explain benefits and one risk with mitigation.", hint="The main benefit is... Another benefit is... A key risk is... To reduce the risk...", sample_answer="The main benefit is faster onboarding. Another benefit is fewer repeated questions. A key risk is it becomes outdated. To reduce the risk, we'll review it monthly and assign an owner.", focus="Benefits + risk + mitigation", expected_keywords=("benefit", "risk", "reduce")),
        CoachTurn(coach="Answer a question and offer follow-up if needed.", hint="That's a good question... I'm not sure yet, but I can follow up by...", sample_answer="That's a good question. As far as I know, it takes about one day. I'm not sure about maintenance yet, but I can follow up by tomorrow.", focus="Q&A", expected_keywords=("good question", "as far as I know", "follow up")),
    ),
    "identifying-assumptions": (
        CoachTurn(coach="We should cut steps to increase conversion.", hint="Surface an assumption politely.", sample_answer="It seems you're assuming fewer steps automatically mean better conversion.", focus="Assumption", expected_keywords=("assuming", "steps", "conversion")),
        CoachTurn(coach="Ask a clarifying question about the premise.", hint="What are we assuming about...?", sample_answer="What are we assuming about user trust and clarity?", focus="Premise", expected_keywords=("assuming", "trust", "clarity")),
        CoachTurn(coach="Make it testable and propose a next step.", hint="If that's true, then... Let's...", sample_answer="If that's true, then we should see drop-offs mainly on longer forms. Let's separate essential steps from redundant ones and measure impact.", focus="Test", expected_keywords=("if that's true", "measure")),
    ),
    "information-discussion-mission": (
        CoachTurn(coach="I just read an article about remote work and productivity. What was the main point?", hint="The article is about... The main point is...", sample_answer="The article is about remote work and productivity. The main point is clear rules improve focus.", focus="Summary", expected_keywords=("article is about", "main point")),
        CoachTurn(coach="Do you think the source is reliable? Why or why not?", hint="I'm not sure it's reliable because... I'd check...", sample_answer="I'm not sure it's reliable because it doesn't cite data. I'd check official reports or reputable outlets.", focus="Reliability", expected_keywords=("reliable", "because", "I'd check")),
        CoachTurn(coach="I found another source that says the opposite. How does that change your view, and what should we do next?", hint="I wasn't aware... That changes things... I'd like to understand... Can you share...?", sample_answer="I wasn't aware of that. That changes things. I'd like to understand the methodology. Can you share the link so we can revise our conclusion?", focus="New info + next steps", expected_keywords=("aware", "changes", "understand", "share")),
    ),
    "invitation-mission": (
        CoachTurn(coach="Do you want to grab coffee tomorrow?", hint="Tolak dengan sopan dan beri alasan singkat.", sample_answer="Thanks, but I can't tomorrow. Something came up.", focus="Decline with a reason", expected_keywords=("can't", "something came up")),
        CoachTurn(coach="No problem. How about Saturday?", hint="Setuju, lalu tanya jamnya.", sample_answer="Saturday is good. What time?", focus="Ask for the time", expected_keywords=("what time", "?")),
        CoachTurn(coach="Does 3 pm work for you?", hint="Setuju dan konfirmasi tempat.", sample_answer="Yes, 3 pm works. Where should we meet?", focus="Confirm time and ask place", expected_keywords=("works", "where should we meet", "?")),
        CoachTurn(coach="Let's meet at the cafe near the station.", hint="Tutup percakapan dengan sopan.", sample_answer="Great. See you then.", focus="Close the plan", expected_keywords=("see you then",)),
    ),
    "inviting-someone": (
        CoachTurn(coach="Do you want to watch a movie tonight?", hint="Reaksi positif, lalu tanya detailnya.", sample_answer="That sounds fun. What time?", focus="React and ask details", expected_keywords=("that sounds fun", "what time", "?")),
        CoachTurn(coach="How about 8 pm?", hint="Setuju, lalu tanya filmnya.", sample_answer="8 pm works. Which movie?", focus="Confirm time", expected_keywords=("works", "which movie", "?")),
        CoachTurn(coach="The new action movie.", hint="Terima ajakan dengan sopan.", sample_answer="Nice. I'd love to go.", focus="Accept politely", expected_keywords=("i'd love to", "go")),
    ),
    "joining-a-simple-meeting": (
        CoachTurn(coach="Any updates before we close?", hint="Minta kesempatan bicara dengan sopan.", sample_answer="I'd like to add one point about the schedule.", focus="Speak up politely", expected_keywords=("like to", "point")),
        CoachTurn(coach="Sure, go ahead.", hint="Sampaikan saran singkat.", sample_answer="I suggest we move the deadline to Thursday to reduce risk.", focus="Give a suggestion", expected_keywords=("suggest", "deadline")),
        CoachTurn(coach="That makes sense. Anything else?", hint="Tutup dan tanya next step.", sample_answer="No. What are the next steps?", focus="Ask for next steps", expected_keywords=("next steps",)),
    ),
    "leadership-coaching-mission": (
        CoachTurn(coach="We're stuck between moving fast and reducing risk. What direction would you set?", hint="The direction I'd like to set is... What options do you see?", sample_answer="The direction I'd like to set is stabilizing billing first. What options do you see right now?", focus="Direction + options", expected_keywords=("direction", "options")),
        CoachTurn(coach="That helps. What's the smallest next step we could take, and what would success look like?", hint="What would success look like? smallest next step?", sample_answer="What would success look like for the pilot, and what's the smallest next step you can take today?", focus="Coach", expected_keywords=("success", "smallest next step")),
        CoachTurn(coach="Given our constraints, which option would you recommend, and can we align on it today?", hint="Given our constraints... Can we agree on...?", sample_answer="Given our constraints, I'd recommend a phased rollout. Can we agree on scope today and review metrics weekly?", focus="Decision", expected_keywords=("constraints", "recommend", "agree")),
    ),
    "making-a-proposal": (
        CoachTurn(coach="What do you propose?", hint="Gunakan I propose we...", sample_answer="I propose we do a small pilot first.", focus="Make proposal", expected_keywords=("propose",)),
        CoachTurn(coach="What's the timeline?", hint="How about we run it for ... weeks?", sample_answer="How about we run it for two weeks and review the results?", focus="Suggest timeline", expected_keywords=("how about", "weeks")),
        CoachTurn(coach="Check if it works for me.", hint="Would that work for you?", sample_answer="Would that work for you?", focus="Check agreement", expected_keywords=("would", "work")),
    ),
    "making-a-simple-decision": (
        CoachTurn(coach="We have two options. What do you prefer?", hint="Gunakan I'd rather + because.", sample_answer="I'd rather fix it now because users are blocked.", focus="State preference with reason", expected_keywords=("rather", "because")),
        CoachTurn(coach="But it's late. Any compromise?", hint="Gunakan We could ...", sample_answer="We could do a quick rollback and review tomorrow.", focus="Suggest compromise", expected_keywords=("could", "rollback")),
        CoachTurn(coach="Okay. What's the decision?", hint="Gunakan Let's ...", sample_answer="Okay, let's roll back now.", focus="Make decision", expected_keywords=("let's",)),
    ),
    "making-an-appointment": (
        CoachTurn(coach="Good morning. Green Clinic. How can I help you?", hint="Minta buat janji (polite).", sample_answer="Hi. I'd like to make an appointment.", focus="Make a polite request", expected_keywords=("i'd like", "appointment")),
        CoachTurn(coach="Sure. What day works for you?", hint="Usulkan waktu.", sample_answer="Is tomorrow afternoon okay?", focus="Suggest a day/time", expected_keywords=("tomorrow", "afternoon")),
        CoachTurn(coach="We have 3:30 p.m. available.", hint="Terima dan konfirmasi.", sample_answer="Great. I'll take it.", focus="Accept the time", expected_keywords=("i'll take", "3:30")),
    ),
    "making-next-step-plans": (
        CoachTurn(coach="What's your next step?", hint="Jawab dengan My next step is to ...", sample_answer="My next step is to practice with Conversation Coach.", focus="State next step", expected_keywords=("next step", "to")),
        CoachTurn(coach="How often will you do it this week?", hint="Jawab dengan ... times this week.", sample_answer="I'll do it three times this week.", focus="Set schedule", expected_keywords=("times", "week")),
        CoachTurn(coach="Great. How will you keep it realistic?", hint="Gunakan keep it simple.", sample_answer="I'm going to keep it simple and do short sessions.", focus="Keep the plan realistic", expected_keywords=("keep", "simple")),
    ),
    "making-plans": (
        CoachTurn(coach="Are you free tomorrow?", hint="Jawab singkat, lalu tanya rencananya.", sample_answer="Yes, I think so. Why?", focus="Check availability", expected_keywords=("True", "why")),
        CoachTurn(coach="Let's get coffee after work.", hint="Tanyakan jamnya dengan pertanyaan pendek.", sample_answer="Sure. What time?", focus="Ask the time", expected_keywords=("what time", "?")),
        CoachTurn(coach="How about 6 pm?", hint="Setuju, lalu tanya tempat ketemunya.", sample_answer="6 pm works for me. Where should we meet?", focus="Confirm and ask place", expected_keywords=("works for me", "where should we meet", "?")),
    ),
    "making-simple-requests": (
        CoachTurn(coach="What do you need?", hint="Minta link dengan sopan.", sample_answer="Can you send me the link, please?", focus="Polite request", expected_keywords=("send", "link", "?")),
        CoachTurn(coach="Yes, of course.", hint="Ucapkan terima kasih.", sample_answer="Thank you.", focus="Thanking", expected_keywords=()),
        CoachTurn(coach="Can you wait a minute?", hint="Terima request untuk menunggu.", sample_answer="Sure. No problem.", focus="Accepting request", expected_keywords=("sure", "problem")),
        CoachTurn(coach="Here is the link.", hint="Tutup dengan thanks.", sample_answer="Great. Thanks.", focus="Closing", expected_keywords=("great",)),
    ),
    "managing-expectations": (
        CoachTurn(coach="Can we deliver the full scope by next week?", hint="Start with what you can commit to.", sample_answer="What we can commit to is a smaller release by next week.", focus="Commitment", expected_keywords=("commit", "smaller")),
        CoachTurn(coach="When can we deliver everything?", hint="The earliest we can deliver... assuming...", sample_answer="The earliest we can deliver the full scope is two weeks later, assuming no new blockers.", focus="Timeline + condition", expected_keywords=("earliest", "assuming", "blockers")),
        CoachTurn(coach="Define success criteria.", hint="Success means...", sample_answer="Success means fewer incidents and a stable rollout with clear monitoring.", focus="Success", expected_keywords=("success means", "stable")),
    ),
    "meeting-participation-mission": (
        CoachTurn(coach="What's the first point you want to bring up today?", hint="I'd like to bring up...", sample_answer="I'd like to bring up the timeline for the next release.", focus="Open topic", expected_keywords=("bring up", "timeline")),
        CoachTurn(coach="Okay. Does this include the admin dashboard work, or is that separate?", hint="Just to clarify... Does this include...? out of scope...", sample_answer="Just to clarify, does this include the admin dashboard changes? If not, that's out of scope for now.", focus="Clarify scope", expected_keywords=("clarify", "include", "out of scope")),
        CoachTurn(coach="Thanks. Before we wrap up, do you have any feedback, and what are the action items?", hint="Overall... I noticed... To summarize... Action items are...", sample_answer="Overall it was clear, but I noticed the intro was long. To summarize, action items are: I'll update the tickets, and you'll confirm the design handoff.", focus="Feedback + summary", expected_keywords=("noticed", "to summarize", "action items")),
    ),
    "negotiation-mission": (
        CoachTurn(coach="What's your top priority?", hint="My top priority is ... + ask mine.", sample_answer="My top priority is quality. What matters most to you?", focus="Priorities", expected_keywords=("top priority", "matters most")),
        CoachTurn(coach="Make a proposal with a timeline.", hint="I propose we ... for ... weeks.", sample_answer="I propose we run a small pilot for two weeks.", focus="Proposal", expected_keywords=("propose", "weeks")),
        CoachTurn(coach="I’m concerned it will delay the launch. Respond and offer a compromise.", hint="I understand the concern. Would it help if... A compromise could be...", sample_answer="I understand the concern. Would it help if we prepare in parallel? A compromise could be launching to 10% first, then expanding if results look good.", focus="Objection + compromise", expected_keywords=("understand", "help", "compromise")),
    ),
    "nuanced-opinion-mission": (
        CoachTurn(coach="Do you think we should standardize the process across all teams?", hint="To some extent... That said...", sample_answer="To some extent, yes—especially for new projects. That said, we need exceptions for legacy systems.", focus="Nuanced stance", expected_keywords=("to some extent", "that said")),
        CoachTurn(coach="Some people say speed matters more, while others worry about stability. How do you see it?", hint="On the one hand... On the other hand... On balance...", sample_answer="On the one hand, speed matters. On the other hand, stability reduces risk. On balance, I'd prioritize stability with a limited rollout.", focus="Balance", expected_keywords=("on the one hand", "on the other hand", "on balance")),
        CoachTurn(coach="I still think a full rollout right now is the best option.", hint="I see your point, but... I might frame it differently...", sample_answer="I see your point, but I'm not sure I'd go that far. I might frame it differently: limited launch first, then full rollout after we review the data.", focus="Soft disagreement", expected_keywords=("see your point", "frame", "limited")),
    ),
    "opening-a-meeting-point": (
        CoachTurn(coach="What would you like to bring up?", hint="Mulai dengan I'd like to bring up...", sample_answer="I'd like to bring up the timeline for the next release.", focus="Open a topic", expected_keywords=("bring up", "timeline")),
        CoachTurn(coach="What's the main point?", hint="Gunakan The main point is...", sample_answer="The main point is we need to confirm the scope today.", focus="State main point", expected_keywords=("main point", "scope")),
        CoachTurn(coach="Thanks. I'd like to hear your thoughts too.", hint="Gunakan I'd like to hear your thoughts.", sample_answer="I'd like to hear your thoughts first, then we can decide.", focus="Invite input", expected_keywords=("hear", "thoughts")),
    ),
    "opinion-conversation-mission": (
        CoachTurn(coach="What do you think about this restaurant?", hint="Jawab dengan opini + because.", sample_answer="I think it's good because it's cheap.", focus="Opinion with reason", expected_keywords=("i think", "because")),
        CoachTurn(coach="Any concern?", hint="Tolak halus: I'm not sure + might be ...", sample_answer="I'm not sure. The service might be slow.", focus="Polite concern", expected_keywords=("not sure", "might")),
        CoachTurn(coach="That's fair. Do you have another idea?", hint="Kasih alternatif + because.", sample_answer="Yes. I think the cafe next door is better because it is quieter.", focus="Suggest alternative with reason", expected_keywords=("better", "because")),
    ),
    "ordering-a-drink": (
        CoachTurn(coach="Hi. What would you like?", hint="Pesan teh dengan sopan.", sample_answer="Can I have a tea, please?", focus="Polite order", expected_keywords=("have", "tea", "?")),
        CoachTurn(coach="Small or large?", hint="Pilih ukuran kecil.", sample_answer="Small, please.", focus="Size choice", expected_keywords=("small",)),
        CoachTurn(coach="Anything else?", hint="Katakan tidak ada lagi dengan sopan.", sample_answer="No, thank you.", focus="Finishing order", expected_keywords=()),
        CoachTurn(coach="Here you go.", hint="Tutup dengan thank you.", sample_answer="Thank you.", focus="Thanking", expected_keywords=()),
    ),
    "past-experience-mission": (
        CoachTurn(coach="Hey! What did you do yesterday?", hint="Jawab dengan tempat + aktivitas (past).", sample_answer="I went to the museum and took photos.", focus="Tell where and what you did", expected_keywords=("went", "took")),
        CoachTurn(coach="Nice. How was it?", hint="Jawab dengan It was + adjective, lalu opini singkat.", sample_answer="It was really interesting. I liked it.", focus="Describe and give opinion", expected_keywords=("it was", "liked")),
        CoachTurn(coach="Did you go with anyone?", hint="Jawab dan sebutkan dengan siapa.", sample_answer="Yes, I went with my friend.", focus="Say who you went with", expected_keywords=("with", "friend")),
    ),
    "personal-story-mission": (
        CoachTurn(coach="Tell me about something interesting that happened recently.", hint="Mulai dengan scene: time + place + who.", sample_answer="Last weekend, I was in Bandung with my cousin.", focus="Start with scene", expected_keywords=("last", "was", "with")),
        CoachTurn(coach="What happened?", hint="Ceritakan 2 event pakai first/then.", sample_answer="First, we explored the city. Then we got lost for a while.", focus="Tell events in order", expected_keywords=("first", "then")),
        CoachTurn(coach="How did you feel?", hint="Sebutkan feeling + contrast (but).", sample_answer="I felt nervous, but after we asked for directions, I felt relieved.", focus="Describe feelings", expected_keywords=("felt", "but", "relieved")),
    ),
    "preference-discussion-mission": (
        CoachTurn(coach="We have two options. Compare them.", hint="Bandingin pakai but.", sample_answer="Option A is easier, but it's more expensive.", focus="Compare options", expected_keywords=("but", "more")),
        CoachTurn(coach="Okay. Which do you prefer and why?", hint="Jawab dengan I prefer ... because ...", sample_answer="I prefer option B because it's cheaper.", focus="Preference with reason", expected_keywords=("prefer", "because")),
        CoachTurn(coach="Give one advantage and one downside, then confirm agreement.", hint="The advantage is... One downside is... So we agree on...?", sample_answer="The advantage is it's healthier. One downside is it takes time. So we agree on option B?", focus="Pros/cons + agreement", expected_keywords=("advantage", "downside", "agree")),
    ),
    "presenting-evidence": (
        CoachTurn(coach="Do we have data to support this?", hint="Use According to...", sample_answer="According to the support dashboard, drop-offs increased after the redesign.", focus="Source", expected_keywords=("according to", "dashboard")),
        CoachTurn(coach="So the redesign caused it?", hint="Clarify correlation vs causation.", sample_answer="To be precise, the data indicates correlation, not necessarily causation.", focus="Precision", expected_keywords=("precise", "correlation", "causation")),
        CoachTurn(coach="Close with a careful implication and another source.", hint="This suggests... Another source shows...", sample_answer="This suggests we should investigate the checkout experience. Session recordings also show confusion on the verification step.", focus="Implication + triangulation", expected_keywords=("suggests", "recordings", "confusion")),
    ),
    "problem-solving-discussion-mission": (
        CoachTurn(coach="Before we jump to solutions, how would you define the problem and scope?", hint="Let's define... Can we agree on the scope?", sample_answer="Let's define the problem statement first. Can we agree on the scope?", focus="Framing", expected_keywords=("define", "scope")),
        CoachTurn(coach="The data shows drop-off after the checkout changes. What could be causing it?", hint="Based on the data... one possible cause is...", sample_answer="Based on the data, one possible cause is confusion in checkout after the redesign.", focus="Causes", expected_keywords=("based on", "data", "possible")),
        CoachTurn(coach="Okay. What trade-off do you see, and what would you recommend next?", hint="The trade-off is... Given these constraints... We can mitigate it by...", sample_answer="The trade-off is speed versus reliability. Given these constraints, I'd recommend a two-week pilot. We can mitigate risk by setting clear metrics and a strict timeline.", focus="Trade-offs + recommendation", expected_keywords=("trade-off", "recommend", "mitigate")),
    ),
    "problem-solving-mission": (
        CoachTurn(coach="Quick check: what's the issue?", hint="Jelaskan problem + impact singkat.", sample_answer="There's a problem with the login page. Users can't sign in.", focus="Describe problem and impact", expected_keywords=("problem", "can't")),
        CoachTurn(coach="What should we do?", hint="Kasih solusi dengan could/should + because.", sample_answer="We could roll back now because it's quick.", focus="Suggest solution with reason", expected_keywords=("could", "because")),
        CoachTurn(coach="But will it affect other features?", hint="Jawab dengan might + next steps (so let's...).", sample_answer="It might, so let's roll back and then test the key flows.", focus="Respond to concern and decide next steps", expected_keywords=("might", "so", "let's")),
    ),
    "qualifying-your-opinion": (
        CoachTurn(coach="Should we adopt the new policy immediately?", hint="Jawab dengan partial agreement + scope.", sample_answer="To some extent, yes—especially for new projects.", focus="Scope", expected_keywords=("to some extent", "especially")),
        CoachTurn(coach="So you're fully in favor?", hint="Broadly speaking... That said...", sample_answer="Broadly speaking, I support it. That said, we need a clear exception for legacy systems.", focus="Limitation", expected_keywords=("broadly", "that said", "exception")),
        CoachTurn(coach="What would you suggest instead?", hint="Propose a phased approach.", sample_answer="I'd phase it in over two quarters and review adoption data along the way.", focus="Suggestion", expected_keywords=("phase", "review")),
    ),
    "reaching-agreement": (
        CoachTurn(coach="We need to decide. What do you suggest?", hint="Usul dengan How about we...", sample_answer="How about we go with the cheaper one tonight?", focus="Make a suggestion", expected_keywords=("how about", "cheaper")),
        CoachTurn(coach="I'm okay with that, but I'm worried it's crowded.", hint="Tanggapi concern pakai might + so let's...", sample_answer="It might be, so let's go early.", focus="Respond to concern", expected_keywords=("might", "so", "let's")),
        CoachTurn(coach="Great. Confirm the agreement.", hint="Konfirmasi: So we agree on ...?", sample_answer="Great. So we agree on Noodle House at 6:30?", focus="Confirm agreement", expected_keywords=("agree", "at")),
    ),
    "reacting-politely": (
        CoachTurn(coach="I'm a bit tired today.", hint="Tunjukkan empati dan tanya balik dengan lembut.", sample_answer="Oh no. Are you okay?", focus="React to a problem", expected_keywords=("are you okay", "?")),
        CoachTurn(coach="Yeah, I'm fine. I didn't sleep well.", hint="Beri respons sopan, lalu tanya singkat tentang kondisi mereka.", sample_answer="I'm sorry to hear that. Do you need a break?", focus="Polite follow-up", expected_keywords=("i'm sorry to hear that", "?")),
        CoachTurn(coach="Thanks. But I finished my project today.", hint="Reaksi positif dan beri pujian singkat.", sample_answer="That's great! Nice work.", focus="React to good news", expected_keywords=("that's great", "nice work")),
    ),
    "reading-context": (
        CoachTurn(coach="The client says the timeline is 'ambitious'. What does that mean?", hint="Interpret cautiously: My sense is that...", sample_answer="My sense is that they're signaling concern without saying no directly.", focus="Interpretation", expected_keywords=("my sense", "signaling", "concern")),
        CoachTurn(coach="What should we do before replying?", hint="Ask to clarify priority.", sample_answer="Before we decide, can we clarify what their priority is—speed or risk reduction?", focus="Clarify", expected_keywords=("before we decide", "clarify", "priority")),
        CoachTurn(coach="Offer a tactful option and set the right tone.", hint="May be worth considering... stay respectful...", sample_answer="It may be worth considering a phased plan to show flexibility. We should stay respectful and avoid sounding defensive.", focus="Option + tone", expected_keywords=("worth considering", "phased", "respectful")),
    ),
    "recommending-a-solution": (
        CoachTurn(coach="We need a recommendation. What should we do?", hint="Given these constraints, I'd recommend...", sample_answer="Given these constraints, I'd recommend starting with a two-week pilot.", focus="Recommend", expected_keywords=("recommend", "pilot")),
        CoachTurn(coach="What's the main risk?", hint="The main risk is... if...", sample_answer="The main risk is slower progress if we over-scope the pilot.", focus="Risk", expected_keywords=("main risk", "if")),
        CoachTurn(coach="How do we mitigate it?", hint="We can mitigate it by...", sample_answer="We can mitigate it by setting clear success metrics and a strict timeline.", focus="Mitigation", expected_keywords=("mitigate", "metrics")),
    ),
    "repairing-misunderstanding": (
        CoachTurn(coach="Acknowledge the misunderstanding and clarify intent.", hint="I may have misunderstood... I didn't mean to...", sample_answer="I may have misunderstood their tone. I didn't mean to come across as dismissive.", focus="Acknowledge", expected_keywords=("misunderstood", "didn't mean", "dismissive")),
        CoachTurn(coach="Clarify what you meant.", hint="Just to clarify, my intent was ...", sample_answer="Just to clarify, my intent was to confirm the constraints, not reject the request.", focus="Clarify intent", expected_keywords=("just to clarify", "intent", "not reject")),
        CoachTurn(coach="Propose a repair plan and timeline.", hint="How about we... I'll draft it...", sample_answer="How about we send a short note acknowledging the misunderstanding and offer a quick call? I'll draft it and share it in ten minutes.", focus="Repair plan", expected_keywords=("how about", "acknowledging", "call", "draft")),
    ),
    "requesting-service-help": (
        CoachTurn(coach="Sure. What do you need?", hint="Tanyakan lokasi barang.", sample_answer="Can you show me where the batteries are?", focus="Ask for a location", expected_keywords=("where", "batteries", "?")),
        CoachTurn(coach="They're over there, next to the cash register.", hint="Konfirmasi dan ucapkan terima kasih.", sample_answer="Great. Thank you for your help.", focus="Thank politely", expected_keywords=("thank", "help")),
        CoachTurn(coach="You're welcome.", hint="Tutup dengan sopan.", sample_answer="Have a good day.", focus="Close politely", expected_keywords=("good day",)),
    ),
    "rescheduling": (
        CoachTurn(coach="Can we reschedule our coffee?", hint="Setuju, lalu tanya sebabnya.", sample_answer="Sure. What happened?", focus="Ask for the reason", expected_keywords=("what happened", "?")),
        CoachTurn(coach="Something came up at work.", hint="Tawarkan waktu baru dengan how about.", sample_answer="No problem. How about Friday evening?", focus="Propose a new time", expected_keywords=("how about", "friday")),
        CoachTurn(coach="Friday is good. Does 7 pm work for you?", hint="Setuju dan konfirmasi tempat.", sample_answer="Yes, 7 pm works. Same cafe?", focus="Confirm time and place", expected_keywords=("works", "same cafe", "?")),
    ),
    "responding-to-advice": (
        CoachTurn(coach="Maybe you should try a small daily goal.", hint="Terima saran dengan sopan.", sample_answer="That sounds good.", focus="Accept advice", expected_keywords=("sounds",)),
        CoachTurn(coach="When will you start?", hint="Jawab dengan rencana singkat.", sample_answer="I'll try that starting tomorrow.", focus="Commit to action", expected_keywords=("try", "tomorrow")),
        CoachTurn(coach="How will you keep it consistent?", hint="Sebutkan satu cara (checklist/alarm).", sample_answer="I'll set a reminder and track it in a checklist.", focus="Plan for consistency", expected_keywords=("reminder", "checklist")),
    ),
    "responding-to-counterpoints": (
        CoachTurn(coach="I like your idea, but I'm worried it will increase costs.", hint="Mulai dengan That's a fair point / I understand the concern.", sample_answer="That's a fair point. However, the long-term savings could be significant.", focus="Acknowledge + respond", expected_keywords=("fair point", "however")),
        CoachTurn(coach="The upfront investment is still high.", hint="Tawarkan mitigasi: phase it in / pilot.", sample_answer="I understand the concern, but we can phase it in and measure results.", focus="Mitigation plan", expected_keywords=("phase", "measure")),
        CoachTurn(coach="Great. What's the next step?", hint="Usul langkah berikutnya.", sample_answer="Let's define success metrics first and run a small pilot.", focus="Next steps", expected_keywords=("metrics", "pilot")),
    ),
    "responding-to-long-turns": (
        CoachTurn(coach="We're dealing with several issues at once: dependencies across teams, time pressure from leadership, and visibility if anything slips.", hint="Let me make sure I got this...", sample_answer="Let me make sure I got this: we need to manage dependencies, time pressure, and stakeholder visibility.", focus="Summary", expected_keywords=("make sure", "got this")),
        CoachTurn(coach="Exactly. We need to keep changes small, communicate clearly, and monitor risk as we go.", hint="The key points are...", sample_answer="The key points are: keep changes small, communicate clearly, and monitor risk.", focus="Key points", expected_keywords=("key points",)),
        CoachTurn(coach="Given all that, what would your response be?", hint="Here's how I'd respond...", sample_answer="Here's how I'd respond: propose phases, share metrics, and set weekly check-ins.", focus="Response", expected_keywords=("here's how", "phases", "weekly")),
    ),
    "responding-to-new-information": (
        CoachTurn(coach="I found a report that contradicts what we read.", hint="I wasn't aware of that.", sample_answer="Oh, I wasn't aware of that.", focus="Acknowledge", expected_keywords=("aware",)),
        CoachTurn(coach="It says the sample size was very small.", hint="That changes things + request understanding.", sample_answer="That changes things. I'd like to understand the methodology.", focus="Update view + ask", expected_keywords=("changes", "understand")),
        CoachTurn(coach="That makes sense. What should we do next?", hint="We should check... Can you share... Then we can revise...", sample_answer="We should check the full report. Can you share the link? Then we can revise our conclusion.", focus="Next steps", expected_keywords=("check", "share", "revise")),
    ),
    "responding-under-pressure": (
        CoachTurn(coach="This is just speculation. Do you have anything solid?", hint="Clarify calmly: indicators, not proof.", sample_answer="Let me be clear: we have indicators, not proof yet.", focus="Clarity", expected_keywords=("be clear", "indicators", "not proof")),
        CoachTurn(coach="So why should we act now?", hint="Acknowledge + key point.", sample_answer="I understand the concern. However, the key point is that waiting increases risk.", focus="Key point", expected_keywords=("understand", "however", "key point")),
        CoachTurn(coach="Show me the numbers and propose next step.", hint="If you look at... doubled... pilot...", sample_answer="If you look at the last four weeks, incident volume has doubled. We run a pilot this week and review results before scaling.", focus="Evidence + proposal", expected_keywords=("last four weeks", "doubled", "pilot")),
    ),
    "review-arguments-and-meetings": (
        CoachTurn(coach="Can you summarize your position?", hint="My position is that...", sample_answer="My position is that we should prioritize fixing the billing flow.", focus="Position", expected_keywords=("position", "prioritize")),
        CoachTurn(coach="What's your main reason?", hint="The main reason is...", sample_answer="The main reason is it affects revenue and support workload.", focus="Reason", expected_keywords=("main reason", "affects")),
        CoachTurn(coach="Close with a summary and next steps.", hint="To summarize... Next steps are...", sample_answer="To summarize, we focus on billing first. Next steps are: I'll share a plan today, and you'll review it by Friday.", focus="Close", expected_keywords=("to summarize", "next steps", "by")),
    ),
    "review-goals-and-preferences": (
        CoachTurn(coach="What's your goal right now?", hint="Goal + by ...", sample_answer="My goal is to speak more confidently by the end of this month.", focus="Goal with deadline", expected_keywords=("goal", "by")),
        CoachTurn(coach="How's it going?", hint="I've been practicing ...", sample_answer="I'm making progress. I've been practicing every morning.", focus="Progress update", expected_keywords=("progress", "been")),
        CoachTurn(coach="Which practice method do you prefer, and why?", hint="I prefer ... because ...", sample_answer="I prefer Conversation Coach because it gives me feedback.", focus="Preference with reason", expected_keywords=("prefer", "because")),
    ),
    "review-health-and-past": (
        CoachTurn(coach="You don't look well. What's wrong?", hint="Bilang kamu nggak enak badan + 1 gejala.", sample_answer="I don't feel well. I have a headache.", focus="Describe symptom", expected_keywords=("feel well", "headache")),
        CoachTurn(coach="Did you sleep late last night?", hint="Jawab yes/no, lalu tambah detail singkat.", sample_answer="Yes. I went to bed late.", focus="Answer past question", expected_keywords=("yes", "late")),
        CoachTurn(coach="And what did you do yesterday?", hint="Jawab dengan 1-2 aktivitas (past).", sample_answer="I went to the clinic and stayed home.", focus="Describe yesterday", expected_keywords=("went", "stayed")),
    ),
    "review-information-and-clients": (
        CoachTurn(coach="Is this report reliable?", hint="Based on the source... verify...", sample_answer="Based on the source, it's a partial snapshot. We should verify it with our support data.", focus="Reliability", expected_keywords=("source", "verify")),
        CoachTurn(coach="Clients are worried about delays. What do you say?", hint="I understand the concern... Just to clarify...", sample_answer="I understand the concern. Just to clarify, what timeline did we promise?", focus="Concern + clarify", expected_keywords=("understand", "clarify", "timeline")),
        CoachTurn(coach="Close with next steps and a deadline.", hint="Next steps are... today... by Friday.", sample_answer="Next steps are: I'll share an update today, and we'll confirm a revised timeline by Friday.", focus="Next steps", expected_keywords=("next steps", "today", "by")),
    ),
    "review-introductions": (
        CoachTurn(coach="Hi, good morning. My name is Omar.", hint="Sapa balik dan sebutkan namamu.", sample_answer="Good morning. My name is Dimas.", focus="Name review", expected_keywords=("morning", "name", "dimas")),
        CoachTurn(coach="Nice to meet you. Where are you from?", hint="Jawab asalmu dengan I'm from ...", sample_answer="I'm from Indonesia.", focus="Origin review", expected_keywords=("i'm", "from", "indonesia")),
        CoachTurn(coach="I live in Jakarta now.", hint="Tanyakan balik dengan How about you?", sample_answer="How about you?", focus="Question back", expected_keywords=("how", "about", "?")),
        CoachTurn(coach="I'm from Malaysia.", hint="Tutup percakapan dengan sopan.", sample_answer="Oh, nice. See you in class.", focus="Closing", expected_keywords=("nice", "see", "class")),
    ),
    "review-leadership-and-listening": (
        CoachTurn(coach="Something feels off, but I can't tell what the real concern is.", hint="What I'm hearing is...", sample_answer="What I'm hearing is there's some concern under the surface.", focus="Mirror", expected_keywords=("hearing", "concern")),
        CoachTurn(coach="I think people are worried about blame, but I'm not sure what that means.", hint="When you say X, do you mean Y or Z?", sample_answer="When you say 'worried about blame', do you mean fear of mistakes or fear of visibility?", focus="Clarify", expected_keywords=("do you mean", "fear")),
        CoachTurn(coach="That makes sense. What would success look like in the next two weeks, and what should we do next?", hint="What would success look like...? Next steps are...", sample_answer="What would success look like in the next two weeks? Next steps are: you'll propose the pilot plan, and I'll help align stakeholders tomorrow.", focus="Criteria + next steps", expected_keywords=("success", "next steps", "tomorrow")),
    ),
    "review-negotiation-and-presenting": (
        CoachTurn(coach="We need this delivered next week.", hint="Mulai dengan Here's my proposal...", sample_answer="Here's my proposal: we deliver a smaller scope next week, then the full version two weeks later.", focus="Proposal", expected_keywords=("proposal", "scope")),
        CoachTurn(coach="What's the trade-off?", hint="The trade-off is...", sample_answer="The trade-off is speed versus completeness.", focus="Trade-off", expected_keywords=("trade-off",)),
        CoachTurn(coach="Close with a recommendation and summary.", hint="I'd recommend... To summarize...", sample_answer="I'd recommend that compromise. To summarize: top two features next week, the rest in two weeks.", focus="Close", expected_keywords=("recommend", "to summarize")),
    ),
    "review-nuance-and-strategy": (
        CoachTurn(coach="Do you support the plan as it is?", hint="On balance... but I'd...", sample_answer="On balance, I support it, but I'd adjust the scope to reduce risk.", focus="Nuance", expected_keywords=("on balance", "scope", "risk")),
        CoachTurn(coach="Okay. To be precise, what would you change?", hint="To be precise...", sample_answer="To be precise, I'd keep the core workflow and postpone optional add-ons.", focus="Precision", expected_keywords=("to be precise", "core", "postpone")),
        CoachTurn(coach="That sounds reasonable. What can you commit to, and what's the next step?", hint="What I can commit to is... Next steps are...", sample_answer="What I can commit to is a pilot next week. Next steps are: I'll share a one-page summary today, and we'll align tomorrow.", focus="Commitment + next steps", expected_keywords=("commit", "next steps", "today")),
    ),
    "review-places-and-shopping": (
        CoachTurn(coach="Excuse me. Can I help you?", hint="Tanyakan lokasi cafe.", sample_answer="Where is the cafe?", focus="Place question", expected_keywords=("where", "cafe", "?")),
        CoachTurn(coach="Go straight and turn right.", hint="Konfirmasi lokasinya dekat library.", sample_answer="Is it next to the library?", focus="Confirm place", expected_keywords=("next", "library", "?")),
        CoachTurn(coach="Yes, it is. Great, you walk there. Now you're at the cafe. What would you like?", hint="Pesan satu teh dengan sopan.", sample_answer="I would like one tea, please.", focus="Order", expected_keywords=("one", "tea")),
        CoachTurn(coach="Sure. It is two dollars.", hint="Bayar dan ucapkan terima kasih.", sample_answer="Here you go. Thank you.", focus="Payment", expected_keywords=()),
    ),
    "review-presenting-and-debate": (
        CoachTurn(coach="Give me the short version of your argument.", hint="Let me frame this...", sample_answer="Let me frame this: the goal is reliability, not just speed.", focus="Frame", expected_keywords=("frame", "goal")),
        CoachTurn(coach="What assumption is that based on?", hint="The core assumption is that...", sample_answer="The core assumption is that incidents cost more than delay.", focus="Assumption", expected_keywords=("assumption", "incidents")),
        CoachTurn(coach="If speed matters most, how would you defend that position in short?", hint="If we accept..., then... In short...", sample_answer="If we accept speed as the priority, then we should time-box a pilot and limit scope. In short: validate with metrics, then expand safely.", focus="Pressure response", expected_keywords=("if", "then", "in short")),
    ),
    "review-problems-and-travel": (
        CoachTurn(coach="What's the issue?", hint="Mulai dengan There's a problem with...", sample_answer="There's a problem with the meeting link.", focus="State problem", expected_keywords=("problem", "with")),
        CoachTurn(coach="What's the impact?", hint="Gunakan so untuk dampak.", sample_answer="People can't join, so we need a new link.", focus="Explain impact", expected_keywords=("can't", "so")),
        CoachTurn(coach="Now say you're late and give an estimate.", hint="I'm running late... I'll be there in about...", sample_answer="I'm running a bit late. I'll be there in about 15 minutes.", focus="Delay + estimate", expected_keywords=("running", "in about")),
    ),
    "review-routines-and-time": (
        CoachTurn(coach="What do you do in the morning?", hint="Sebutkan satu rutinitas dan jam.", sample_answer="I wake up at six.", focus="Routine time", expected_keywords=()),
        CoachTurn(coach="Nice. Do you study English after that?", hint="Jawab dengan Yes, lalu sebutkan jam belajar.", sample_answer="Yes, I study English at seven.", focus="Study routine", expected_keywords=()),
        CoachTurn(coach="Good. We have speaking class this week.", hint="Tanyakan kapan kelas speaking.", sample_answer="When is our speaking class?", focus="Class schedule question", expected_keywords=()),
        CoachTurn(coach="It is on Tuesday at eight.", hint="Tutup dengan See you then.", sample_answer="Great. See you then.", focus="Closing", expected_keywords=()),
    ),
    "review-social-and-plans": (
        CoachTurn(coach="Hey! Long time no see. How have you been?", hint="Jawab singkat, lalu balas tanya.", sample_answer="Pretty good. How about you?", focus="Small talk response", expected_keywords=("pretty", "how about")),
        CoachTurn(coach="Busy with work. What have you been working on?", hint="Jawab singkat dengan 1 topik.", sample_answer="I've been working on a new project.", focus="Answer follow-up", expected_keywords=("working on", "project")),
        CoachTurn(coach="Do you want to grab coffee this weekend?", hint="Terima, lalu usulkan waktu.", sample_answer="Sure. Are you free on Saturday afternoon?", focus="Accept and propose time", expected_keywords=("free", "saturday")),
    ),
    "review-stories-and-work": (
        CoachTurn(coach="Tell me about your weekend.", hint="Ceritain 2 kalimat (visited/went...).", sample_answer="It was great. I visited my cousin and we went to a small concert.", focus="Tell a short story", expected_keywords=("visited", "went")),
        CoachTurn(coach="What happened after that?", hint="Jawab pakai then.", sample_answer="Then we grabbed street food and talked until late.", focus="Continue the story", expected_keywords=("then",)),
        CoachTurn(coach="Now give a work update and next step.", hint="I'm working on... Next, I'll...", sample_answer="I'm working on the release checklist. Next, I'll review the risks.", focus="Work update + next step", expected_keywords=("working on", "next")),
    ),
    "review-travel-and-shopping": (
        CoachTurn(coach="Hi. Can I help you?", hint="Tanya lokasi atau jadwal.", sample_answer="Yes, please. What time is the next train?", focus="Ask travel question", expected_keywords=("what time", "train")),
        CoachTurn(coach="It's at 4:15. Anything else?", hint="Tanya barang (availability).", sample_answer="Yes. Do you have a phone charger?", focus="Ask availability", expected_keywords=("do you have", "charger")),
        CoachTurn(coach="Sure. What kind do you need?", hint="Sebutkan jenisnya.", sample_answer="A USB-C charger, please.", focus="Specify type", expected_keywords=("usb", "please")),
    ),
    "routine-conversation-mission": (
        CoachTurn(coach="What time do you wake up?", hint="Sebutkan jam bangun.", sample_answer="I wake up at six.", focus="Wake-up time", expected_keywords=("wake", "six")),
        CoachTurn(coach="When do you study English?", hint="Sebutkan hari dan jam.", sample_answer="I study on Monday and Wednesday at seven.", focus="Study schedule", expected_keywords=("study", "monday", "wednesday", "seven")),
        CoachTurn(coach="Is the class online?", hint="Jawab dengan yes/no lengkap.", sample_answer="Yes, it is online.", focus="Class format", expected_keywords=("online",)),
        CoachTurn(coach="Great. See you on Monday.", hint="Tutup percakapan.", sample_answer="See you.", focus="Closing", expected_keywords=("see",)),
    ),
    "saying-hello-and-goodbye": (
        CoachTurn(coach="Hi. Good morning. How are you today?", hint="Jawab sapaan, lalu beri respons singkat.", sample_answer="Good morning. I'm good, thank you. How are you?", focus="Greeting response", expected_keywords=("good morning", "morning", "hi", "hello", "thank", "thanks"), indonesian_explanation="Jawabanmu sudah masuk konteks. Akan lebih natural kalau menambahkan pertanyaan balik singkat."),
        CoachTurn(coach="Nice. What is your name?", hint="Sebutkan nama dengan pola: My name is ... atau I'm ...", sample_answer="My name is Arif. Nice to meet you.", focus="Self introduction", expected_keywords=("my name is", "i'm", "i am", "nice to meet"), indonesian_explanation="Untuk perkenalan, pola 'My name is ...' atau 'I'm ...' sudah cukup. Tambahkan 'Nice to meet you' agar lebih ramah."),
        CoachTurn(coach="Nice to meet you. Where are you from?", hint="Jawab asalmu, lalu tambahkan pertanyaan balik sederhana.", sample_answer="I'm from Indonesia. How about you?", focus="Follow-up question", expected_keywords=("from", "indonesia", "jakarta", "how about you", "?"), indonesian_explanation="Saat menjawab asal, tambahkan pertanyaan balik seperti 'How about you?' supaya percakapan terus berjalan."),
    ),
    "saying-how-you-feel": (
        CoachTurn(coach="Hey, are you okay?", hint="Jawab singkat, lalu bilang kamu nggak enak badan.", sample_answer="Not really. I don't feel well.", focus="Say you feel unwell", expected_keywords=("don't feel well", "not really")),
        CoachTurn(coach="What's wrong?", hint="Sebutkan satu gejala.", sample_answer="I have a headache.", focus="Name a symptom", expected_keywords=("have", "headache")),
        CoachTurn(coach="Do you want to go home?", hint="Jawab, lalu tambahkan satu gejala lagi.", sample_answer="Yes. I think I have a fever.", focus="Add another symptom", expected_keywords=("think", "fever")),
    ),
    "saying-what-you-can-do": (
        CoachTurn(coach="Can you speak English?", hint="Sebutkan kemampuanmu dengan I can.", sample_answer="I can speak a little.", focus="Speaking ability", expected_keywords=("speak", "little")),
        CoachTurn(coach="Can you write simple emails?", hint="Jawab dengan Yes, I can.", sample_answer="Yes, I can.", focus="Writing ability", expected_keywords=()),
        CoachTurn(coach="Can you join a meeting in English?", hint="Gunakan Not yet kalau belum bisa.", sample_answer="Not yet, but I can try.", focus="Honest ability", expected_keywords=("not", "yet", "but", "try")),
    ),
    "saying-what-you-do": (
        CoachTurn(coach="What do you do?", hint="Jawab dengan status sederhana.", sample_answer="I'm a student.", focus="Work or study status", expected_keywords=("i'm", "student")),
        CoachTurn(coach="What do you study?", hint="Sebutkan subjek yang kamu pelajari.", sample_answer="I study design.", focus="Study subject", expected_keywords=("study", "design")),
        CoachTurn(coach="Do you study online?", hint="Jawab dengan yes/no lengkap.", sample_answer="Yes, I study online.", focus="Study format", expected_keywords=("study", "online")),
    ),
    "saying-what-you-think": (
        CoachTurn(coach="Oh yeah? What did you think?", hint="Kasih opini singkat: I think it's + adjective.", sample_answer="I think it's really good.", focus="Give an opinion", expected_keywords=("i think", "it's")),
        CoachTurn(coach="What did you like about it?", hint="Sebutkan satu hal: story/actor/music.", sample_answer="I liked the story. It was fun.", focus="Add a comment", expected_keywords=("liked",)),
        CoachTurn(coach="Would you recommend it?", hint="Jawab yes/no + alasan singkat.", sample_answer="Yes, I would. It is simple, but fun.", focus="Recommend with reason", expected_keywords=("yes", "but")),
    ),
    "saying-what-you-want": (
        CoachTurn(coach="What do you want?", hint="Sebutkan kamu mau sandwich.", sample_answer="I want a sandwich.", focus="Want statement", expected_keywords=("want", "sandwich")),
        CoachTurn(coach="Do you want tea or coffee?", hint="Pilih tea dengan sopan.", sample_answer="Tea, please.", focus="Choosing option", expected_keywords=("tea",)),
        CoachTurn(coach="Do you want sugar?", hint="Katakan tanpa gula.", sample_answer="No sugar, please.", focus="No extra item", expected_keywords=("sugar",)),
    ),
    "saying-where-you-are-from": (
        CoachTurn(coach="Where are you from?", hint="Jawab dengan pola: I'm from ...", sample_answer="I'm from Indonesia.", focus="Origin", expected_keywords=("from", "indonesia", "jakarta", "bandung", "surabaya"), indonesian_explanation="Untuk asal negara atau kota, gunakan pola 'I'm from ...' dengan singkat dan jelas."),
        CoachTurn(coach="Where do you live now?", hint="Gunakan pola: I live in ...", sample_answer="I live in Jakarta.", focus="Current city", expected_keywords=("live in", "jakarta", "bandung", "surabaya"), indonesian_explanation="Bedakan origin dan tempat tinggal sekarang: 'I'm from ...' dan 'I live in ...'."),
        CoachTurn(coach="Nice. How about you?", hint="Tanyakan balik dengan: How about you?", sample_answer="How about you?", focus="Question back", expected_keywords=("how about you", "where are you from", "?"), indonesian_explanation="Pertanyaan balik seperti 'How about you?' menjaga percakapan tetap berjalan."),
    ),
    "saying-where-you-went": (
        CoachTurn(coach="Hi! Did you go anywhere interesting yesterday?", hint="Jawab, lalu bilang kamu pergi ke mana.", sample_answer="Yes, I went to the museum.", focus="Say where you went", expected_keywords=("went", "to")),
        CoachTurn(coach="Oh nice. Where did you go after that?", hint="Sebutkan tempat kedua.", sample_answer="I went to a cafe near the river.", focus="Add another place", expected_keywords=("went", "cafe")),
        CoachTurn(coach="Sounds relaxing. Where did you go?", hint="Balik tanya.", sample_answer="Where did you go?", focus="Ask back", expected_keywords=("where", "did")),
    ),
    "saying-you-do-not-understand": (
        CoachTurn(coach="Please open your book.", hint="Katakan kamu tidak mengerti.", sample_answer="Sorry, I don't understand.", focus="Saying confusion", expected_keywords=("sorry", "don't", "understand")),
        CoachTurn(coach="That's okay. I can say it again.", hint="Minta diulangi dengan sopan.", sample_answer="Can you repeat that, please?", focus="Asking repetition", expected_keywords=("repeat", "?")),
        CoachTurn(coach="Yes. Open your book.", hint="Konfirmasi instruksi.", sample_answer="Open my book?", focus="Confirmation", expected_keywords=("open", "book", "?")),
        CoachTurn(coach="Yes, that's right.", hint="Katakan sudah paham.", sample_answer="Thank you. I understand now.", focus="Closing", expected_keywords=("understand",)),
    ),
    "saying-your-name": (
        CoachTurn(coach="Hi, my name is Omar. What is your name?", hint="Jawab dengan pola: My name is ... atau I'm ...", sample_answer="My name is Arif. Nice to meet you.", focus="Saying your name", expected_keywords=("my name is", "i'm", "i am", "nice to meet"), indonesian_explanation="Sebutkan nama dengan satu kalimat jelas, lalu tambahkan respons ramah seperti 'Nice to meet you'."),
        CoachTurn(coach="Nice to meet you. What should I call you?", hint="Gunakan pola: Please call me ...", sample_answer="Please call me Arif.", focus="Nickname", expected_keywords=("please call me", "call me"), indonesian_explanation="Kalau ingin menyebut nama panggilan, gunakan pola pendek 'Please call me ...'."),
        CoachTurn(coach="Great. Nice to meet you, Arif.", hint="Balas dengan sopan: Nice to meet you too.", sample_answer="Nice to meet you too.", focus="Polite response", expected_keywords=("nice to meet you too", "you too"), indonesian_explanation="Untuk membalas sapaan perkenalan, 'Nice to meet you too' sudah natural dan sopan."),
    ),
    "setting-direction": (
        CoachTurn(coach="What should the team focus on this sprint?", hint="Set direction clearly.", sample_answer="The direction I'd like to set is stabilizing the billing flow first.", focus="Direction", expected_keywords=("direction", "first")),
        CoachTurn(coach="How do we define success?", hint="Success looks like...", sample_answer="Success looks like fewer incidents and faster completion rates.", focus="Success", expected_keywords=("success", "incidents")),
        CoachTurn(coach="Assign ownership and boundaries.", hint="I'd like you to own... Let's align on scope...", sample_answer="I'd like you to own the rollout plan, and I'll own stakeholder updates. Let's align on scope and keep it time-boxed to two weeks.", focus="Ownership + scope", expected_keywords=("own", "scope", "time-boxed")),
    ),
    "setting-the-scene": (
        CoachTurn(coach="You look happy today. What happened?", hint="Mulai dengan kapan + di mana.", sample_answer="Last weekend, I was in Bandung.", focus="Set time and place", expected_keywords=("last", "was", "in")),
        CoachTurn(coach="Oh nice. Who were you with?", hint="Jawab dengan with + person.", sample_answer="I was there with my cousin.", focus="Say who you were with", expected_keywords=("with", "cousin")),
        CoachTurn(coach="What were you doing there?", hint="Tambah 1 aktivitas background.", sample_answer="We were visiting my aunt and exploring the city.", focus="Add background activity", expected_keywords=("were", "visiting")),
    ),
    "sharing-email-addresses": (
        CoachTurn(coach="What is your email address?", hint="Sebutkan email dengan at dan dot.", sample_answer="It's ben dot rama at example dot com.", focus="Giving an email address", expected_keywords=("it's", "ben", "dot", "rama")),
        CoachTurn(coach="Can you spell that, please?", hint="Eja bagian nama email pelan-pelan.", sample_answer="B-E-N dot R-A-M-A.", focus="Spelling an email", expected_keywords=("dot",)),
        CoachTurn(coach="Is that correct?", hint="Konfirmasi dengan: Yes, that's correct.", sample_answer="Yes, that's correct.", focus="Confirming an email", expected_keywords=("that's", "correct")),
    ),
    "shopping-service-mission": (
        CoachTurn(coach="Hi. Can I help you?", hint="Jelaskan barang yang kamu cari.", sample_answer="Yes, please. I'm looking for a USB-C charger.", focus="Ask for an item", expected_keywords=("i'm looking for", "charger")),
        CoachTurn(coach="Sure. We have this one and that one.", hint="Bandingkan dua opsi dengan pertanyaan.", sample_answer="Which one is cheaper?", focus="Compare options", expected_keywords=("cheaper", "?")),
        CoachTurn(coach="This one is cheaper.", hint="Pilih satu opsi dengan singkat.", sample_answer="Okay. I'll take this one.", focus="Choose an option", expected_keywords=("i'll take",)),
        CoachTurn(coach="Anything else?", hint="Minta bantuan cari barang lain.", sample_answer="Yes. Could you help me? Where are the batteries?", focus="Request help", expected_keywords=("could you help me", "where", "?")),
    ),
    "signposting-clearly": (
        CoachTurn(coach="Start with a signposting opener.", hint="Let me walk you through...", sample_answer="Let me quickly walk you through the plan.", focus="Opener", expected_keywords=("walk you through",)),
        CoachTurn(coach="Use first, next, finally to outline your structure.", hint="First... Next... Finally...", sample_answer="First, I'll explain the problem. Next, I'll share the proposal. Finally, I'll outline next steps.", focus="Structure", expected_keywords=("first", "next", "finally")),
        CoachTurn(coach="Wrap up with a short summary phrase.", hint="Let me summarize...", sample_answer="Let me summarize the key points in one sentence.", focus="Summary", expected_keywords=("summarize",)),
    ),
    "simple-place-words": (
        CoachTurn(coach="Where are you going?", hint="Sebutkan kamu pergi ke cafe.", sample_answer="I'm going to the cafe.", focus="Destination", expected_keywords=("i'm", "going", "cafe")),
        CoachTurn(coach="Is the cafe near here?", hint="Jawab dan sebutkan dekat library.", sample_answer="Yes. It is near the library.", focus="Nearby place", expected_keywords=("near", "library")),
        CoachTurn(coach="I am going to the library.", hint="Ajak pergi bersama.", sample_answer="Let's go together.", focus="Friendly suggestion", expected_keywords=("let's", "together")),
    ),
    "small-talk-mission": (
        CoachTurn(coach="Hi! How's it going?", hint="Jawab singkat, lalu tanya balik.", sample_answer="Hi! I'm good, thanks. How about you?", focus="Start the chat", expected_keywords=("i'm good", "thanks", "how about you", "?")),
        CoachTurn(coach="I'm a bit tired today.", hint="Tunjukkan empati dan tanya sebabnya dengan simple past.", sample_answer="I'm sorry to hear that. Did you sleep well?", focus="Ask about the reason", expected_keywords=("i'm sorry to hear that", "did you", "?")),
        CoachTurn(coach="Not really. I stayed up late.", hint="Pindah topik dengan halus, lalu ajak buat rencana weekend.", sample_answer="Oh okay. By the way, any plans for the weekend?", focus="Change topic and plan", expected_keywords=("by the way", "any plans for the weekend", "?")),
        CoachTurn(coach="I'm going to a new cafe on Saturday at 3 pm. Do you want to join?", hint="Terima ajakan dan konfirmasi waktu dengan singkat.", sample_answer="That sounds fun. Great, see you then!", focus="Accept and close", expected_keywords=("that sounds fun", "see you")),
    ),
    "softening-disagreement": (
        CoachTurn(coach="We should launch next week, no matter what.", hint="Acknowledge + soften.", sample_answer="I see your point, but I'm not sure I'd go that far.", focus="Soften", expected_keywords=("see your point", "not sure")),
        CoachTurn(coach="Explain your concern respectfully.", hint="With respect... suggests...", sample_answer="With respect, the current error rate suggests we're not ready.", focus="Evidence", expected_keywords=("with respect", "suggests")),
        CoachTurn(coach="Offer an alternative plan.", hint="I might frame it differently...", sample_answer="I might frame it differently: we launch a limited version next week and keep the rest behind a feature flag.", focus="Alternative", expected_keywords=("frame", "limited", "feature flag")),
    ),
    "spelling-your-name": (
        CoachTurn(coach="Hi. What is your name?", hint="Sebutkan namamu dengan pola: My name is ... atau I'm ...", sample_answer="My name is Dimas.", focus="Saying your name clearly", expected_keywords=("my name is", "i'm", "i am", "dimas"), indonesian_explanation="Sebutkan nama dengan satu kalimat pendek dan jelas. Pola 'My name is ...' sudah cukup untuk konteks registrasi."),
        CoachTurn(coach="How do you spell it?", hint="Eja nama huruf demi huruf, lalu boleh ulangi namanya.", sample_answer="It's spelled D-I-M-A-S.", focus="Spelling your name", expected_keywords=("spelled", "d-i-m-a-s", "dimas"), indonesian_explanation="Saat diminta mengeja, sebutkan huruf satu per satu dengan jeda pendek. Kamu bisa memakai pola 'It's spelled ...'."),
        CoachTurn(coach="Thank you. Let me read it back: D-I-M-A-S.", hint="Konfirmasi bahwa ejaannya benar.", sample_answer="That's right.", focus="Confirming spelling", expected_keywords=("that's right", "right", "yes"), indonesian_explanation="Untuk mengonfirmasi ejaan, 'That's right' terdengar natural dan sopan."),
    ),
    "starting-small-talk": (
        CoachTurn(coach="Hi! How's your day?", hint="Jawab singkat, lalu tanya balik dengan sopan.", sample_answer="Hi! It's pretty good, thanks. How about you?", focus="Start small talk", expected_keywords=("pretty good", "thanks", "how about you", "?")),
        CoachTurn(coach="Pretty good. It's busy today. How about you?", hint="Katakan kondisi harimu (mis. busy/okay) dengan satu kalimat pendek.", sample_answer="I'm good. It's a bit busy too.", focus="Describe your day", expected_keywords=("i'm good", "busy")),
        CoachTurn(coach="Nice. By the way, how was your weekend?", hint="Jawab tentang weekend dengan 1 kegiatan sederhana.", sample_answer="It was nice. I went to the park.", focus="Weekend follow-up", expected_keywords=("it was", "nice", "went to")),
    ),
    "stating-your-position": (
        CoachTurn(coach="What's your position on switching to written updates?", hint="Mulai dengan In my view / I believe.", sample_answer="In my view, a written update would be better for routine topics.", focus="State position", expected_keywords=("in my view", "better")),
        CoachTurn(coach="Why?", hint="Jawab dengan because + satu alasan.", sample_answer="Because it saves time and helps people focus.", focus="Give reason", expected_keywords=("because", "time")),
        CoachTurn(coach="But some people want real-time discussion.", hint="Acknowledge + but + solusi singkat.", sample_answer="I see your point, but we can keep one live meeting per month.", focus="Respond to counterpoint", expected_keywords=("see your point", "but")),
    ),
    "strategic-workplace-mission": (
        CoachTurn(coach="We're under pressure to deliver soon, but we can't afford a messy rollout.", hint="To make sure we're aligned... top priority... biggest constraint...", sample_answer="To make sure we're aligned, what's your top priority and biggest constraint?", focus="Align", expected_keywords=("aligned", "priority", "constraint")),
        CoachTurn(coach="Top priority is reducing incidents, and the biggest constraint is time.", hint="What we can commit to is... by... assuming...", sample_answer="What we can commit to is a smaller release by next week, assuming no critical blockers appear.", focus="Expectations", expected_keywords=("commit", "assuming")),
        CoachTurn(coach="Okay, but what's the main risk if we do that, and how would you mitigate it?", hint="The main risk is... We can mitigate it by...", sample_answer="The main risk is incidents during rollout. We can mitigate it by time-boxing the rollout, adding monitoring, and having a rollback plan.", focus="Risk", expected_keywords=("main risk", "mitigate", "rollback")),
    ),
    "structuring-a-short-presentation": (
        CoachTurn(coach="Open your presentation.", hint="Today I'd like to...", sample_answer="Today I'd like to share an idea to improve our onboarding.", focus="Opening", expected_keywords=("today", "idea")),
        CoachTurn(coach="State the problem and proposal.", hint="The problem is... My proposal is...", sample_answer="The problem is new hires feel lost. My proposal is a simple checklist and a buddy system.", focus="Problem + proposal", expected_keywords=("problem", "proposal")),
        CoachTurn(coach="Close with next steps.", hint="Next steps are...", sample_answer="Next steps are: draft the checklist today, then pilot it with the next hire.", focus="Next steps", expected_keywords=("next steps", "draft", "pilot")),
    ),
    "suggesting-a-solution": (
        CoachTurn(coach="Any ideas to fix it?", hint="Kasih saran dengan could.", sample_answer="We could roll back the update.", focus="Suggest a solution", expected_keywords=("could", "roll")),
        CoachTurn(coach="Why?", hint="Jawab dengan because + reason.", sample_answer="Because rollback is quick and low risk.", focus="Give a reason", expected_keywords=("because",)),
        CoachTurn(coach="How can we prevent it next time?", hint="Gunakan should + so.", sample_answer="We should add a quick test so it doesn't happen again.", focus="Preventive step", expected_keywords=("should", "so")),
    ),
    "summarizing-an-article": (
        CoachTurn(coach="What's the article about?", hint="The article is about ...", sample_answer="The article is about how remote work affects productivity.", focus="Topic", expected_keywords=("article is about",)),
        CoachTurn(coach="What's the main point?", hint="The main point is ...", sample_answer="The main point is productivity improves with clear communication rules.", focus="Main point", expected_keywords=("main point",)),
        CoachTurn(coach="How does it conclude?", hint="It concludes that ...", sample_answer="It concludes that hybrid setups work best for many teams.", focus="Conclusion", expected_keywords=("concludes",)),
    ),
    "summarizing-decisions": (
        CoachTurn(coach="Before we finish, what did we decide?", hint="Gunakan To summarize...", sample_answer="To summarize, we agreed to keep scope limited to the core feature.", focus="Summarize decision", expected_keywords=("to summarize", "agreed")),
        CoachTurn(coach="Good. Who owns the action items?", hint="Action items are: I'll..., you'll...", sample_answer="Action items are: I'll update the tickets, and you'll confirm the design handoff.", focus="Action items", expected_keywords=("action items", "I'll", "you'll")),
        CoachTurn(coach="Great. When should we check progress again?", hint="We'll check progress on ...", sample_answer="We'll check progress on Thursday.", focus="Next checkpoint", expected_keywords=("check progress",)),
    ),
    "summarizing-what-you-heard": (
        CoachTurn(coach="We've discussed the timeline, client concerns, and rollout risk. Can you summarize where we are?", hint="So, to summarize...", sample_answer="So, to summarize: the timeline is tight and clients are sensitive to change.", focus="Summary", expected_keywords=("to summarize", "timeline")),
        CoachTurn(coach="Good. Now what's the decision, and what are the open questions?", hint="The decision is... The open questions are...", sample_answer="The decision is to propose a phased rollout with clear metrics. The open questions are around resourcing and internal alignment.", focus="Decision + open questions", expected_keywords=("decision", "open questions")),
        CoachTurn(coach="That sounds close. Can you confirm it one more time before we close?", hint="Just to confirm... Does that capture it...?", sample_answer="Just to confirm, does that capture it accurately?", focus="Confirm", expected_keywords=("confirm", "capture")),
    ),
    "supporting-with-reasons": (
        CoachTurn(coach="Why should we invest in automated tests?", hint="Mulai dengan One reason is...", sample_answer="One reason is it reduces bugs in production.", focus="Reason 1", expected_keywords=("one reason", "reduces")),
        CoachTurn(coach="What's another reason?", hint="Gunakan Another reason is...", sample_answer="Another reason is it speeds up releases because we can deploy with more confidence.", focus="Reason 2", expected_keywords=("another reason", "because")),
        CoachTurn(coach="But writing tests takes time.", hint="Acknowledge + but + solusi singkat.", sample_answer="That's true, but we can start small and it saves time later.", focus="Address concern", expected_keywords=("that's true", "but")),
    ),
    "talking-about-daily-routines": (
        CoachTurn(coach="What do you do in the morning?", hint="Sebutkan kegiatan dan waktunya.", sample_answer="I wake up at six.", focus="Morning routine", expected_keywords=("wake", "six")),
        CoachTurn(coach="What do you do after that?", hint="Gunakan after that untuk kegiatan berikutnya.", sample_answer="I study English at seven.", focus="Next routine step", expected_keywords=("study", "english", "seven")),
        CoachTurn(coach="Do you work in the afternoon?", hint="Jawab ya/tidak lalu beri waktu.", sample_answer="Yes, I work at one.", focus="Afternoon routine", expected_keywords=("work", "one")),
    ),
    "talking-about-goals": (
        CoachTurn(coach="What's your goal this month?", hint="Jawab dengan: My goal is to ...", sample_answer="My goal is to speak more confidently.", focus="State the goal", expected_keywords=("goal", "to")),
        CoachTurn(coach="By when?", hint="Gunakan by + waktu.", sample_answer="By the end of this month.", focus="State the deadline", expected_keywords=("by", "end")),
        CoachTurn(coach="Why does it matter to you?", hint="Jawab dengan because + reason.", sample_answer="Because I want to join meetings without feeling nervous.", focus="Give a reason", expected_keywords=("because", "meetings")),
    ),
    "talking-about-likes": (
        CoachTurn(coach="Do you like English?", hint="Jawab dengan: Yes, I like it.", sample_answer="Yes, I like it.", focus="Simple preference", expected_keywords=()),
        CoachTurn(coach="What do you like?", hint="Sebutkan bagian belajar yang kamu suka.", sample_answer="I like speaking practice.", focus="Learning preference", expected_keywords=("speaking", "practice")),
        CoachTurn(coach="Do you like grammar?", hint="Jawab jujur dengan kalimat pendek.", sample_answer="It's okay, but speaking is my favorite.", focus="Favorite part", expected_keywords=("it's", "but", "speaking", "favorite")),
    ),
    "talking-about-local-habits": (
        CoachTurn(coach="Tell me a local habit in your area.", hint="Mulai dengan People usually...", sample_answer="People usually eat outside in the evening.", focus="Describe habit", expected_keywords=("usually",)),
        CoachTurn(coach="Can you give an example?", hint="Gunakan In my area, people often...", sample_answer="In my area, people often grab noodles or satay after work.", focus="Give example", expected_keywords=("often", "in my area")),
        CoachTurn(coach="How often does it happen?", hint="Tambahkan detail: especially on weekends.", sample_answer="Especially on weekends.", focus="Add frequency detail", expected_keywords=("especially", "weekends")),
    ),
    "talking-about-weekends": (
        CoachTurn(coach="Any plans for the weekend?", hint="Jawab dengan going to + satu aktivitas.", sample_answer="Yes. I'm going to visit my parents.", focus="Share a plan", expected_keywords=("i'm going to", "visit")),
        CoachTurn(coach="Nice. Where do they live?", hint="Jawab tempatnya dengan singkat.", sample_answer="They live in Bandung.", focus="Give a detail", expected_keywords=("they live in", "bandung")),
        CoachTurn(coach="Sounds good. How are you getting there?", hint="Jawab transportnya, lalu tutup dengan sopan.", sample_answer="I'm taking the train. Have a great weekend.", focus="Transport and closing", expected_keywords=("i'm taking", "train", "have a great weekend")),
    ),
    "talking-about-yesterday": (
        CoachTurn(coach="Hey, how was your day yesterday?", hint="Jawab singkat (good/okay), lalu bilang kamu pergi ke mana.", sample_answer="It was good. I went to the mall.", focus="Answer and say where you went", expected_keywords=("was", "went")),
        CoachTurn(coach="Nice. What did you do there?", hint="Sebutkan 1-2 aktivitas (past verb).", sample_answer="I bought a jacket and ate ramen.", focus="Describe past activities", expected_keywords=("bought", "ate")),
        CoachTurn(coach="Did you go alone?", hint="Jawab dan sebutkan dengan siapa.", sample_answer="No, I went with my brother.", focus="Say who you went with", expected_keywords=("with", "brother")),
    ),
    "talking-to-a-driver": (
        CoachTurn(coach="Hi. Where to?", hint="Sebutkan tujuan dengan sopan.", sample_answer="Can you take me to the station, please?", focus="Say the destination", expected_keywords=("take me to", "station")),
        CoachTurn(coach="Sure. To the station.", hint="Tanya durasi perjalanannya.", sample_answer="Thanks. How long will it take?", focus="Ask travel time", expected_keywords=("how long", "?")),
        CoachTurn(coach="About 20 minutes.", hint="Buat satu request sopan.", sample_answer="Okay. Please take the fastest route.", focus="Make a request", expected_keywords=("please", "fastest")),
    ),
    "telling-events-in-order": (
        CoachTurn(coach="So what did you do on your trip?", hint="Mulai dengan first.", sample_answer="First, we checked in at the hotel.", focus="Start the sequence", expected_keywords=("first",)),
        CoachTurn(coach="Nice. What did you do next?", hint="Gunakan then atau after that.", sample_answer="Then we walked around and tried street food.", focus="Continue the sequence", expected_keywords=("then",)),
        CoachTurn(coach="And finally?", hint="Tutup dengan finally + reason singkat.", sample_answer="Finally, we went back early because we were tired.", focus="End the sequence", expected_keywords=("finally", "because")),
    ),
    "telling-the-time": (
        CoachTurn(coach="What time is the class?", hint="Jawab dengan pola: It's at ...", sample_answer="It's at nine o'clock.", focus="Class time", expected_keywords=("it's", "nine", "o'clock")),
        CoachTurn(coach="In the morning?", hint="Konfirmasi bagian hari.", sample_answer="Yes, in the morning.", focus="Time of day", expected_keywords=("morning",)),
        CoachTurn(coach="Thank you.", hint="Balas dengan sopan.", sample_answer="You're welcome.", focus="Polite reply", expected_keywords=("you're", "welcome")),
    ),
    "transport-mission": (
        CoachTurn(coach="Hi. Where are you going?", hint="Minta tiket dan sebutkan tujuan.", sample_answer="I'd like one ticket to Bandung, please.", focus="Ticket request", expected_keywords=("i'd like", "ticket")),
        CoachTurn(coach="One-way or round-trip?", hint="Pilih satu-way.", sample_answer="One-way, please.", focus="Ticket type", expected_keywords=("one-way",)),
        CoachTurn(coach="Okay. It leaves at 6:30 pm from platform 2.", hint="Tanya balik platform atau durasi dengan singkat.", sample_answer="Great. Which platform again?", focus="Confirm details", expected_keywords=("platform", "?")),
        CoachTurn(coach="Hi. Where to?", hint="Minta driver antar ke hotel.", sample_answer="Can you take me to my hotel, please?", focus="Driver request", expected_keywords=("take me to", "hotel")),
    ),
    "travel-situation-mission": (
        CoachTurn(coach="Hi. Are you on your way to the hotel?", hint="Jelaskan kamu telat + alasan + estimasi.", sample_answer="Yes, but I'm running a bit late. My train is delayed. I'll be there in about 20 minutes.", focus="Delay explanation with estimate", expected_keywords=("running", "delayed", "in about")),
        CoachTurn(coach="Okay. Do you have a reservation?", hint="Jawab dengan under + name.", sample_answer="Yes. I have a reservation under Faris Kim.", focus="Confirm reservation", expected_keywords=("reservation", "under")),
        CoachTurn(coach="Great. Anything else you need?", hint="Tanya rekomendasi + minta bantuan dengan could you.", sample_answer="Do you have any recommendations for dinner? If there's a problem with my room, could you help me?", focus="Ask recommendations and request help", expected_keywords=("recommendations", "could you", "problem")),
    ),
    "understanding-client-needs": (
        CoachTurn(coach="We want to improve our product experience.", hint="Mulai dengan pertanyaan klarifikasi (Just to clarify...).", sample_answer="Got it. Just to clarify, who is the main user group?", focus="Clarify user group", expected_keywords=("clarify", "user")),
        CoachTurn(coach="The main users are new hires. What's next?", hint="Minta detail pain point.", sample_answer="Thanks. Could you share more about the biggest pain point today?", focus="Ask for pain point", expected_keywords=("share more", "pain point")),
        CoachTurn(coach="They can't find key docs. Summarize and confirm.", hint="So what you need is ... right?", sample_answer="Understood. So what you need is a clear starting point and a simple checklist, right?", focus="Summarize need", expected_keywords=("need", "right")),
    ),
    "understanding-simple-directions": (
        CoachTurn(coach="Where is the meeting room?", hint="Tanyakan lokasi meeting room.", sample_answer="Where is the meeting room?", focus="Room question", expected_keywords=("where", "meeting", "room", "?")),
        CoachTurn(coach="Go straight.", hint="Ulangi arahan pertama.", sample_answer="Okay. Go straight.", focus="Repeating direction", expected_keywords=("straight",)),
        CoachTurn(coach="Then turn left.", hint="Konfirmasi turn left.", sample_answer="Turn left?", focus="Direction confirmation", expected_keywords=("turn", "left", "?")),
        CoachTurn(coach="Yes. The room is on the right.", hint="Katakan kamu mengerti.", sample_answer="Thank you. I understand.", focus="Understanding", expected_keywords=("understand",)),
    ),
    "using-examples": (
        CoachTurn(coach="Why should onboarding be more structured?", hint="Because... + For example...", sample_answer="Because new hires need clarity. For example, last quarter three new joiners felt lost in week one.", focus="Use an example", expected_keywords=("because", "for example")),
        CoachTurn(coach="What's the impact?", hint="Gunakan so untuk dampak.", sample_answer="So they kept asking in multiple channels and it slowed the team down.", focus="Explain impact", expected_keywords=("so", "kept")),
        CoachTurn(coach="Give a specific suggestion.", hint="Gunakan such as...", sample_answer="Such as pairing each new hire with one mentor for two weeks.", focus="Give specific suggestion", expected_keywords=("such as", "mentor")),
    ),
    "using-precise-transitions": (
        CoachTurn(coach="Your explanation is clear so far. What's next?", hint="Use That brings me to...", sample_answer="That brings me to the key trade-off: speed versus reliability.", focus="Transition", expected_keywords=("brings me to", "trade-off")),
        CoachTurn(coach="Highlight the key point.", hint="What's crucial here is...", sample_answer="What's crucial here is that we set clear standards early.", focus="Key point", expected_keywords=("crucial", "standards")),
        CoachTurn(coach="Restate it and propose a next step.", hint="To put it differently... With that in mind...", sample_answer="To put it differently, standards let teams move fast without breaking consistency. With that in mind, I'd propose a pilot with strict guardrails.", focus="Restate + propose", expected_keywords=("differently", "with that in mind", "pilot")),
    ),
    "work-study-conversation-mission": (
        CoachTurn(coach="Do you work or study?", hint="Sebutkan kerja atau studi.", sample_answer="I study English online.", focus="Work or study", expected_keywords=("study", "english", "online")),
        CoachTurn(coach="What do you like about English?", hint="Sebutkan bagian yang kamu suka.", sample_answer="I like speaking practice.", focus="Preference", expected_keywords=("speaking", "practice")),
        CoachTurn(coach="What can you do in English?", hint="Sebutkan satu kemampuan.", sample_answer="I can introduce myself.", focus="Ability", expected_keywords=("introduce", "myself")),
        CoachTurn(coach="Great. Keep practicing.", hint="Balas dengan singkat dan positif.", sample_answer="Thank you. I will.", focus="Closing", expected_keywords=("will",)),
    ),
    "workplace-mission": (
        CoachTurn(coach="Hi. Quick update on the report?", hint="Mulai dengan progress singkat.", sample_answer="I'm making good progress. I'm almost done with the summary.", focus="Give update", expected_keywords=("progress", "almost")),
        CoachTurn(coach="Great. Please update the risk section too.", hint="Terima, lalu minta klarifikasi scope.", sample_answer="Sure. Could you clarify which risks you want me to focus on?", focus="Ask clarification", expected_keywords=("clarify", "focus")),
        CoachTurn(coach="Focus on timeline and budget risks.", hint="Konfirmasi deadline singkat.", sample_answer="Got it. Just to confirm, you need it by Friday morning, right?", focus="Confirm deadline", expected_keywords=("confirm", "by")),
    ),
}
