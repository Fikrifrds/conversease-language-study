#!/usr/bin/env python3
"""Generate one copy-paste visual prompt pack for every English lesson."""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ENGLISH_ROOT = REPO_ROOT / "content" / "curriculum" / "english"
OUTPUT_ROOT = (
    REPO_ROOT
    / "content"
    / "visual-prompts"
    / "english"
)
LEVEL_ORDER = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4}
FEMALE_VOICE_MARKERS = ("woman", "girl", "lady", "female")

MALE_STYLES = (
    "an olive long-sleeved modest shirt, loose dark trousers ending above the ankle bones, visible socks, and closed shoes",
    "a navy long-sleeved modest shirt, loose beige trousers ending above the ankle bones, visible socks, and closed shoes",
    "a warm gray long-sleeved modest shirt, loose dark trousers ending above the ankle bones, visible socks, and closed shoes",
    "a muted brown long-sleeved modest shirt, loose charcoal trousers ending above the ankle bones, visible socks, and closed shoes",
)
FEMALE_STYLES = (
    "an olive full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
    "a navy full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
    "a warm taupe full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
    "a muted plum full-length khimar covering the chest, a loose opaque abaya, socks, and closed shoes",
)

BackgroundSpec = tuple[str, str, str]

# Every English unit has an explicitly reviewed background. These exact keys replace
# the old keyword matcher, which could confuse a destination being discussed with the
# place where the conversation is actually happening.
UNIT_BACKGROUND_SPECS: dict[tuple[str, str], BackgroundSpec] = {
    ("A1", "unit-01-greeting-introducing-yourself"): (
        "a bright open English classroom beside the classroom entrance",
        "a blank whiteboard, two learner desks, notebooks, and a small plant; the doorway remains visibly open",
        "This is a first meeting before or after class, not a home, private room, ceremony, or formal presentation.",
    ),
    ("A1", "unit-02-spelling-numbers-contact"): (
        "a public language-center registration counter",
        "a blank enrollment form, clipboard, pen, keyboard, and phone placed as registration tools, all without readable characters",
        "This is course registration, not a bank, post office, immigration desk, or casual phone call.",
    ),
    ("A1", "unit-03-daily-routine-time"): (
        "an open classroom schedule-planning corner",
        "a clock face with hands but no numerals, a weekly planner made only of colored blocks, and study books",
        "The speakers are discussing routines and schedules now; do not turn the image into a bedroom, kitchen, morning montage, or literal meeting already in progress.",
    ),
    ("A1", "unit-04-work-study-and-preferences"): (
        "an open language-center study table",
        "notebooks, a closed laptop, headphones, and simple study materials that suggest work and learning choices",
        "This is a classmate conversation about work, study, preferences, and abilities, not a factory, job interview, or private social date.",
    ),
    ("A1", "unit-05-places-directions"): (
        "an outdoor public campus orientation point at a path junction",
        "an abstract line-only area map, clear path branches, and simple directional arrows with no words, buildings, or landmark icons",
        "The speakers are asking how to reach a destination; do not place them inside the destination or show religious buildings, statues, or labeled signs.",
    ),
    ("A1", "unit-06-food-shopping-prices"): (
        "a public café service counter connected to a small retail shelf",
        "a cup, water dispenser, simple packaged items, and blank price holders without numbers or logos",
        "Show the purchase or order taking place at the counter, not people already eating a full meal at a dining table.",
    ),
    ("A1", "unit-07-help-problems-requests"): (
        "an open learning-center help desk",
        "a blank form, pen, small study device, and neatly arranged task materials that make the request visible",
        "This is a small everyday learning problem, not an emergency, police station, hospital crisis, or private room.",
    ),
    ("A1", "unit-08-a1-review-final"): (
        "an open language assessment studio",
        "one orderly task table holding a blank form, clock hands without numerals, an abstract route map, and one simple shop or café item",
        "Keep the review in one coherent assessment setting; do not create a collage of unrelated rooms or literal flashbacks.",
    ),
    ("A2", "unit-01-social-small-talk"): (
        "a bright open office break area beside a shared corridor",
        "two mugs, a small side table, a blank wall planner, and personal work bags",
        "This is brief workplace small talk, not a formal meeting, restaurant meal, party, or private home visit.",
    ),
    ("A2", "unit-02-plans-and-invitations"): (
        "a public learning-center lobby planning corner",
        "a blank event notice card, calendar blocks without text, and two simple location photo cards without people",
        "The speakers are making, accepting, declining, or rescheduling a future plan; do not depict them already attending the event.",
    ),
    ("A2", "unit-03-travel-and-transport"): (
        "a public intermodal transport hub",
        "a ticket counter, abstract platform symbols, a line-only station map, luggage, and a sheltered taxi pickup visible beyond the entrance",
        "Show the current transport question or transaction, not arrival at the final hotel or destination.",
    ),
    ("A2", "unit-04-shopping-services"): (
        "a tidy public department-store service area",
        "organized product shelves, a comparison table, blank size and price holders, and a service counter",
        "Show choosing or requesting help before purchase; do not depict a market crowd, branded shop, or completed home delivery.",
    ),
    ("A2", "unit-05-health-and-appointments"): (
        "a bright public clinic reception and waiting area",
        "a reception counter, blank appointment card, wall clock without numerals, and simple non-graphic health props",
        "Keep the scene calm and non-graphic; do not show surgery, injury, exposed body parts, a hospital emergency, or a private bedroom.",
    ),
    ("A2", "unit-06-past-experiences"): (
        "an open public park pavilion where friends can talk",
        "a bench, small table, travel keepsake, and an object connected to the story such as a plain food container or ticket shape without text",
        "Show the present conversation about yesterday, not a literal flashback, restaurant recreation, or multiple-event montage.",
    ),
    ("A2", "unit-07-opinions-and-reasons"): (
        "a public community-lounge decision table",
        "two topic cards showing objects or landscapes only, a blank cinema-style card, a food photo card, and a simple travel map without labels",
        "The speakers are comparing opinions before deciding; do not place them inside the film, destination, or restaurant being discussed.",
    ),
    ("A2", "unit-08-a2-review-final"): (
        "an open practical-language assessment studio",
        "a travel bag, abstract station map, two shop products, blank appointment card, and planning cards arranged as one exercise station",
        "Keep all review topics inside one coherent practice setting; do not create a collage, flashback montage, or several disconnected locations.",
    ),
    ("B1", "unit-01-personal-stories"): (
        "a quiet open public lounge arranged for a present-day conversation",
        "a notebook, one neutral keepsake, and a few object-only photo cards that can support a story without showing people",
        "Show one person telling a past story to the other now; do not recreate the past event as the current location or add flashback panels.",
    ),
    ("B1", "unit-02-workplace-conversations"): (
        "an open manager-and-team workspace",
        "a shared worktable, laptop with blank screen, task cards without writing, folders, and a simple progress diagram made of shapes",
        "This is an active work update or clarification, not a job interview, classroom, or closed executive office.",
    ),
    ("B1", "unit-03-problems-and-solutions"): (
        "an open workplace problem-solving table",
        "one clearly relevant problem object, two solution cards represented by shapes, and a simple decision marker",
        "Show the speakers diagnosing and deciding together; do not depict an emergency, argument, repair workshop, or unrelated presentation.",
    ),
    ("B1", "unit-04-travel-situations"): (
        "a bright public hotel reception and guest-information area",
        "a reception counter, luggage, blank reservation card, abstract street map, and guest-service objects",
        "The hotel is the conversation base; never confuse a recommended place, delayed train, or guest-room problem with the exact place where the current exchange occurs.",
    ),
    ("B1", "unit-05-goals-and-progress"): (
        "an open learning and coaching studio",
        "a goal board made only of shapes, progress blocks, a blank weekly planner, practice books, and two next-step cards",
        "Show a present planning conversation, not a graduation scene, sports event, literal career outcome, or private tutoring room.",
    ),
    ("B1", "unit-06-explaining-preferences"): (
        "a public decision-making table in a community workspace",
        "two clearly separated option cards, matching object samples, and a central agreement marker without text",
        "The options are being discussed before a decision; do not place the speakers inside either restaurant, office arrangement, or destination mentioned as an option.",
    ),
    ("B1", "unit-07-community-and-culture"): (
        "an open outdoor neighborhood information pavilion",
        "a neutral streetscape, park greenery, local shopfront shapes without signs, and object-only community activity cards",
        "Show a respectful conversation about community and habits; avoid costumes, flags, monuments, religious places, ritual scenes, or cultural stereotypes.",
    ),
    ("B1", "unit-08-b1-review-final"): (
        "an open B1 conversation assessment workspace",
        "a story notebook, progress board, problem-and-solution cards, travel bag, and two choice cards arranged around one table",
        "Keep the connected review in one present conversation; do not make a multi-location montage or literalize every topic mentioned.",
    ),
    ("B2", "unit-01-clear-arguments"): (
        "an open team decision room",
        "a central discussion table, two evidence cards, a blank process diagram, and one next-step marker",
        "Show a structured professional argument about a work process, not a courtroom, political rally, public debate stage, or personal confrontation.",
    ),
    ("B2", "unit-02-professional-meetings"): (
        "an open professional meeting room with a glass corridor visible",
        "a blank agenda board, scope boundary diagram made of shapes, action cards, and neatly arranged chairs",
        "Show the specific meeting phase in the dialogue; do not depict a presentation stage, classroom, private executive office, or social meal.",
    ),
    ("B2", "unit-03-negotiation-and-compromise"): (
        "an open professional negotiation room",
        "two proposal folders, a visual timeline made of blocks, priority tokens, and a central compromise card without words",
        "Show a collaborative work negotiation, not haggling in a market, legal signing ceremony, conflict, or handshake.",
    ),
    ("B2", "unit-04-presenting-ideas"): (
        "an open professional presentation room",
        "a blank screen with abstract chart shapes, a standing presentation table, question cards, and rows of chairs",
        "Show the relevant presentation or Q&A moment; do not add readable slides, an auditorium crowd, award ceremony, or entertainment stage.",
    ),
    ("B2", "unit-05-media-and-information"): (
        "a public library media-review workspace",
        "several textless article sheets, source-comparison cards, reference books with blank spines, and a laptop with abstract data shapes",
        "Show people evaluating information, not a newsroom broadcast, social-media feed, political rally, or literal scene from the article.",
    ),
    ("B2", "unit-06-customer-and-client-communication"): (
        "an open professional client-service meeting alcove",
        "a needs map made of shapes, two option cards, risk markers, a pilot timeline, and a blank next-step plan",
        "Show a service consultation, not a retail checkout, complaint counter, contract-signing ceremony, or private executive office.",
    ),
    ("B2", "unit-07-complex-problem-solving"): (
        "an open workplace problem-solving workshop",
        "a blank problem frame, cause-and-effect shapes, two option boards, trade-off markers, and a recommendation card",
        "Show analytical collaboration around one work problem, not a laboratory experiment, emergency response, repair shop, or argumentative debate.",
    ),
    ("B2", "unit-08-b2-review-final"): (
        "an open professional assessment boardroom",
        "an argument board, meeting agenda shapes, negotiation timeline, source cards, and a client plan arranged as one integrated case",
        "Keep the final task as one coherent professional case discussion, not a collage of meetings, calls, presentations, and unrelated rooms.",
    ),
    ("C1", "unit-01-nuanced-opinions"): (
        "an open strategy discussion room",
        "two viewpoint cards, a balance diagram, certainty markers, and a shared conclusion card without words",
        "Show careful professional reasoning, not a political debate, courtroom, media interview, or hostile confrontation.",
    ),
    ("C1", "unit-02-strategic-workplace-communication"): (
        "an open cross-team strategy room",
        "stakeholder lanes made of colored shapes, constraint markers, a risk matrix without labels, and a shared decision area",
        "Show alignment and risk communication, not a boardroom power struggle, public speech, disciplinary hearing, or closed private office.",
    ),
    ("C1", "unit-03-advanced-presentations"): (
        "an open advanced-presentation studio",
        "a large blank screen with layered abstract diagrams, evidence cards, transition arrows, a question area, and rows of chairs",
        "Show a complex presentation or Q&A, not a lecture crowd, television studio, entertainment stage, or slide full of readable writing.",
    ),
    ("C1", "unit-04-debate-and-analysis"): (
        "an open moderated analysis room",
        "a shared evidence table, assumption cards, a logic-flow diagram made of shapes, and two calm discussion positions",
        "Show evidence-based professional debate, not a political event, courtroom, shouting match, combat pose, or audience spectacle.",
    ),
    ("C1", "unit-05-cross-cultural-professionalism"): (
        "an open international professional training center",
        "blank message cards, neutral workplace objects, a time-sequence diagram, and a shared clarification board",
        "Show workplace communication across contexts without flags, national costumes, skin-tone stereotypes, religious symbols, ceremonies, or tourist landmarks.",
    ),
    ("C1", "unit-06-leadership-and-coaching"): (
        "an open leadership coaching studio",
        "a direction board made of shapes, ownership cards, option-and-trade-off tokens, and a next-step planner without text",
        "Show supportive coaching and decision guidance, not a performance review hearing, classroom lecture, motivational stage, or private closed office.",
    ),
    ("C1", "unit-07-advanced-listening-response"): (
        "an open quiet meeting-recap room",
        "headphones resting on the table, an abstract audio-wave shape, summary cards, concern markers, and follow-up cards without words",
        "Show careful listening and response in the present, not a recording studio, podcast set, surveillance room, or literal replay of earlier events.",
    ),
    ("C1", "unit-08-c1-review-final"): (
        "an open executive-language assessment room",
        "a strategy frame, evidence cards, risk markers, coaching questions, listening-summary cards, and a decision plan arranged as one case",
        "Keep the final conversation as one coherent complex professional scenario, not a collage, debate stage, presentation auditorium, or multiple disconnected scenes.",
    ),
}

LESSON_BACKGROUND_OVERRIDES: dict[tuple[str, str, str], BackgroundSpec] = {
    ("A1", "unit-05-places-directions", "lesson-01-asking-where-a-place-is"): (
        "an outdoor public campus information point before the destination",
        "a line-only map, two branching paths, and a destination marker shown only as a plain geometric block",
        "The location is being asked about; do not place the speakers inside it or draw a labeled sign, landmark, statue, or religious building.",
    ),
    ("A1", "unit-05-places-directions", "lesson-02-simple-place-words"): (
        "an open neighborhood orientation plaza",
        "several neutral building blocks, a road, a park shape, and position markers without labels",
        "Use generic civic shapes only; no real landmarks, flags, worship buildings, signs, or people beyond the permitted cast.",
    ),
    ("A1", "unit-05-places-directions", "lesson-03-understanding-simple-directions"): (
        "an outdoor pedestrian path junction",
        "a visible left turn, right turn, straight path, and simple arrow markers without words",
        "Show the route decision before arrival; do not show the destination interior or use road-sign text.",
    ),
    ("A1", "unit-05-places-directions", "lesson-04-asking-how-to-get-there"): (
        "an open transit-stop map point before a walking route",
        "a line-only route diagram, a start dot, one turn arrow, and a distant generic destination block",
        "The speakers are planning the route; do not show them already traveling, driving, or standing inside the destination.",
    ),
    ("A1", "unit-05-places-directions", "lesson-05-finding-a-place-mission"): (
        "an outdoor campus orientation point connecting several paths",
        "one coherent line-only map with start, turns, and destination dots plus visible matching paths",
        "Keep the complete mission at the route-planning point; do not create multiple panels or show arrival inside the destination.",
    ),
    ("A1", "unit-06-food-shopping-prices", "lesson-01-ordering-a-drink"): (
        "a public café ordering counter",
        "a cup, water pitcher, drink dispenser, and blank menu tiles with no writing, numbers, or logos",
        "Show ordering before the drink is served; do not place the speakers at a dining table or show a full meal.",
    ),
    ("A1", "unit-06-food-shopping-prices", "lesson-02-asking-about-prices"): (
        "a public shop checkout counter",
        "one clearly visible item, a blank price holder, a simple payment tray, and an uncluttered product shelf",
        "Show the price question before purchase; do not render currency symbols, numbers, receipts, logos, or a café meal.",
    ),
    ("A1", "unit-06-food-shopping-prices", "lesson-03-buying-a-simple-item"): (
        "a small public retail shop counter",
        "one basic item being selected, two shelf alternatives, a reusable bag, and a blank checkout display",
        "Show one simple purchase; do not turn the scene into a restaurant, supermarket crowd, or home delivery.",
    ),
    ("A1", "unit-06-food-shopping-prices", "lesson-04-saying-what-you-want"): (
        "a public café service counter before ordering",
        "two simple drink or snack options, a tray, and object-only menu cards without words",
        "Show the speaker indicating a preference at the counter; do not depict eating, a banquet, or a restaurant dining room.",
    ),
    ("A1", "unit-06-food-shopping-prices", "lesson-05-cafe-and-shop-mission"): (
        "a public café kiosk with an attached take-away retail shelf",
        "a drink station, one packaged item, a blank price holder, payment tray, and reusable bag",
        "Keep ordering and buying in one coherent kiosk transaction; do not create separate café and shop panels.",
    ),
    ("A2", "unit-03-travel-and-transport", "lesson-01-buying-a-ticket"): (
        "a public train-station ticket counter before the journey",
        "a blank ticket card, payment tray, luggage, and a rail symbol made only of abstract shapes",
        "Show buying the ticket; do not place the speakers on the train, platform, destination city, or hotel.",
    ),
    ("A2", "unit-03-travel-and-transport", "lesson-02-asking-about-departure-time"): (
        "a public station information point inside the concourse",
        "a clock face with hands but no numerals, abstract platform blocks, a blank ticket, and luggage",
        "Show checking time and platform before boarding; do not depict the moving train, destination, or arrival.",
    ),
    ("A2", "unit-03-travel-and-transport", "lesson-03-checking-directions"): (
        "a station-concourse junction before the gate or platform",
        "a line-only floor map, directional arrows, branching corridors, and abstract platform shapes without labels",
        "The gate or platform is still ahead; do not place the speakers at the destination, inside a vehicle, or beside readable signage.",
    ),
    ("A2", "unit-03-travel-and-transport", "lesson-04-talking-to-a-driver"): (
        "a sheltered public taxi pickup area beside a stationary vehicle",
        "one parked car with an open visible passenger door, luggage, and a generic destination card without words",
        "Show the conversation before departure while both speakers are safely outside or beside the stationary vehicle; do not depict driving or a private enclosed ride.",
    ),
    ("A2", "unit-03-travel-and-transport", "lesson-05-transport-mission"): (
        "a single public intermodal terminal forecourt linking a station entrance and taxi rank",
        "a ticket counter visible through the open station entrance, clock hands without numerals, platform arrows, luggage, and one stationary taxi",
        "Combine the ticket, timing, platform, and taxi steps in one coherent transport hub; do not show the hotel or use a multi-panel montage.",
    ),
    ("A2", "unit-04-shopping-services", "lesson-01-asking-for-an-item"): (
        "a public retail aisle beside a service counter",
        "an organized shelf with one obvious empty product space, several neutral products, and a blank inventory screen",
        "Show asking whether an item is available; do not depict checkout, home delivery, or unrelated clothing fitting.",
    ),
    ("A2", "unit-04-shopping-services", "lesson-02-asking-about-size-and-color"): (
        "a public clothing-store display area",
        "two modest folded garments in distinct muted colors, blank size markers, a mirror showing no reflection, and a service counter",
        "Show choosing size and color; do not depict a fitting room, exposed body, fashion runway, or branded clothing.",
    ),
    ("A2", "unit-04-shopping-services", "lesson-03-comparing-simple-options"): (
        "a public shop comparison table",
        "exactly two neutral products side by side, blank feature cards, and an undecided shopping basket",
        "Show comparison before choosing; do not add many products, price numbers, advertising, or a checkout transaction.",
    ),
    ("A2", "unit-04-shopping-services", "lesson-04-requesting-service-help"): (
        "a public store service point opening directly onto the product aisles",
        "an abstract aisle map, a requested item sample, blank size markers, and a clear path toward the relevant shelf",
        "Show staff guidance inside the store; do not place the speakers at checkout, outside the shop, or in a private fitting room.",
    ),
    ("A2", "unit-04-shopping-services", "lesson-05-shopping-service-mission"): (
        "a public department-store service area beside a comparison display",
        "a requested item, two color or size options, a two-product comparison table, and an abstract aisle guide",
        "Keep finding, comparing, and requesting help in one store zone; do not create a collage or show a completed purchase at home.",
    ),
    ("A2", "unit-05-health-and-appointments", "lesson-01-saying-how-you-feel"): (
        "an open public park pavilion where one friend checks on another",
        "a bench, water bottle, tissues, and a bag, with calm daylight and no medical equipment",
        "This is a friend conversation before seeking care, not a clinic consultation, bedroom, medical emergency, or graphic illness scene.",
    ),
    ("A2", "unit-05-health-and-appointments", "lesson-02-describing-simple-symptoms"): (
        "a bright public clinic consultation desk with an open corridor visible",
        "a blank symptom card, clock hands without numerals, tissues, and simple non-graphic medical objects",
        "Show a calm verbal symptom description; no examination, exposed body, injury, medicine branding, or emergency treatment.",
    ),
    ("A2", "unit-05-health-and-appointments", "lesson-03-making-an-appointment"): (
        "a clear split scene with the caller in an open home-study corner and the receptionist at a public clinic counter",
        "each speaker holds a phone; the clinic side has a blank appointment grid and clock hands without numerals",
        "They are in separate locations connected by phone; do not place them together, show a private bedroom, or depict medical treatment.",
    ),
    ("A2", "unit-05-health-and-appointments", "lesson-04-confirming-details"): (
        "a clear split phone-call scene with Raka in an open home-study corner and the receptionist at a public clinic counter",
        "both speakers hold phones; the clinic side has a blank appointment card, calendar blocks, and clock hands without numerals",
        "They are confirming time, name, and contact details remotely. Do not place them together, show a private bedroom, depict treatment, or render readable personal data.",
    ),
    ("A2", "unit-05-health-and-appointments", "lesson-05-health-appointment-mission"): (
        "a public clinic check-in counter opening onto the waiting area",
        "a blank appointment card, check-in clipboard, tissues, and a non-graphic symptom card",
        "Keep check-in and the short symptom summary at reception; do not move into an examination room or show medical procedures.",
    ),
    ("A2", "unit-07-opinions-and-reasons", "lesson-01-saying-what-you-think"): (
        "a public cinema-lobby discussion corner after a screening",
        "a blank ticket shape and an abstract object-only movie poster with no faces, title, logo, or text",
        "Show the speakers discussing a film after watching it; do not recreate a movie scene or place them inside the auditorium.",
    ),
    ("A2", "unit-07-opinions-and-reasons", "lesson-02-giving-simple-reasons"): (
        "a public community-lounge table used to compare dining options",
        "one object-only restaurant photo card, a plain menu card without text, and two reason markers",
        "They are discussing a restaurant from elsewhere; do not place them inside that restaurant, eating its food, or speaking to restaurant staff.",
    ),
    ("A2", "unit-07-opinions-and-reasons", "lesson-03-agreeing-and-disagreeing-politely"): (
        "a public community-lounge discussion table",
        "two food option cards showing objects only and simple agree-or-compare markers without symbols or words",
        "Show a polite conversation about food preferences, not a meal, cooking scene, restaurant, or heated argument.",
    ),
    ("A2", "unit-07-opinions-and-reasons", "lesson-04-asking-for-opinions"): (
        "a public travel-planning desk before any trip",
        "two landscape-only destination cards, a line-only map, and a blank calendar card",
        "The destination is still being chosen; do not place the speakers at either destination or add flags, monuments, temples, or landmark icons.",
    ),
    ("A2", "unit-07-opinions-and-reasons", "lesson-05-opinion-conversation-mission"): (
        "a public community-lounge dining-choice table",
        "two object-only dining photo cards, neutral reason markers, and a shared choice card without text",
        "They are choosing where to eat before going there; do not depict a restaurant interior, meal, kitchen, or service counter.",
    ),
    ("A2", "unit-08-a2-review-final", "lesson-02-review-travel-and-shopping"): (
        "a public station retail kiosk beside the concourse",
        "a line-only station map, clock hands without numerals, luggage, one shop item, and blank size options",
        "Keep the travel question and shopping request in one plausible station kiosk; do not create separate station and store panels.",
    ),
    ("B1", "unit-04-travel-situations", "lesson-01-checking-in"): (
        "a bright public hotel reception counter immediately after arrival",
        "luggage beside the guest, a blank reservation card and identity-card shape, room-key sleeve, and breakfast icon made only of objects",
        "Show check-in at reception; do not place the speakers in a guest room, restaurant, train station, or private office.",
    ),
    ("B1", "unit-04-travel-situations", "lesson-02-explaining-a-delay"): (
        "a split phone-call scene with Faris in a public station waiting zone and Ilham in an open hotel lobby or workplace reception",
        "both hold phones; Faris has luggage and a stationary train-status board made only of abstract delay shapes, while Ilham has a blank schedule card",
        "They are physically separate during the delay call; do not show them face to face, on a moving train, or already checking in.",
    ),
    ("B1", "unit-04-travel-situations", "lesson-03-asking-for-recommendations"): (
        "a bright public hotel guest-information desk beside the open lobby entrance, before Faris leaves for dinner",
        "Faris has luggage or a room-key sleeve; Ilham indicates a line-only street map and two object-only local-food photo cards; the map contains only streets, a route dot, and turn arrows",
        "This conversation gives a recommendation and walking directions before the visit. Do not place them inside any restaurant, at a dining table, eating, cooking, or already at the recommended place. Do not draw buildings, monuments, labels, flags, or religious icons on the map.",
    ),
    ("B1", "unit-04-travel-situations", "lesson-04-handling-a-simple-complaint"): (
        "a public hotel guest-service counter in the open lobby",
        "a room-key sleeve, a small tabletop air-conditioning control or fan icon, a blank maintenance card, and luggage kept nearby",
        "The guest reports the room problem at the service counter; do not place both speakers alone inside the guest room or show a repair already happening.",
    ),
    ("B1", "unit-04-travel-situations", "lesson-05-travel-situation-mission"): (
        "a split phone-call scene with Faris delayed at a public station and Ilham at the open hotel reception",
        "Faris has luggage and a phone; Ilham has a blank reservation card, room-key sleeve, local-food photo card, and simple guest-help card at the reception counter",
        "The current exchange happens by phone before arrival and previews later hotel needs. Do not place them together, inside a restaurant, inside a guest room, or in a multi-panel sequence of future events.",
    ),
    ("B2", "unit-06-customer-and-client-communication", "lesson-04-confirming-next-steps"): (
        "a split professional phone-call scene with Faris in an open consultant workspace and Ilham in an open client-team office",
        "both speakers use phones; each side shows matching pilot blocks, a blank timeline, review cards, and a next-meeting marker without text",
        "They are confirming a plan remotely. Do not place them in the same room, depict a contract-signing ceremony, or show the future rollout already happening.",
    ),
    ("B2", "unit-06-customer-and-client-communication", "lesson-05-client-conversation-mission"): (
        "a split professional phone-call scene connecting an open consultant workspace and an open client-team office",
        "both speakers use phones; the two sides share matching needs shapes, option cards, concern markers, pilot blocks, and a blank next-step timeline",
        "The full client exchange happens remotely in the present. Do not place the speakers together, literalize the future onboarding rollout, or create separate panels for every discussion stage.",
    ),
    ("B2", "unit-08-b2-review-final", "lesson-03-review-information-and-clients"): (
        "a split professional phone-call scene connecting a media-review workstation and an open client office",
        "the review side has textless source cards and reliability markers; both sides have phones, concern cards, and a matching next-step plan",
        "The source review supports the client call. Do not create a newsroom, show a social-media feed, place the speakers together, or depict future actions as completed.",
    ),
}

REMOTE_SITUATIONS = {
    "making_a_clinic_appointment_by_phone",
    "confirming_an_appointment_details",
    "explaining_travel_delay",
    "mission_travel_delay_check_in_and_help",
    "confirming_next_steps_with_client",
    "mission_client_conversation",
    "review_information_client_call",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate external-image prompts and upload folders for English lessons."
    )
    parser.add_argument("--check", action="store_true", help="Check generated files without writing.")
    args = parser.parse_args(argv)

    generated: dict[Path, str] = {}
    index_rows: list[dict[str, str]] = []
    for lesson_dir in lesson_dirs():
        prompt_path = output_dir(lesson_dir) / "PROMPT.md"
        generated[prompt_path] = build_prompt(lesson_dir)
        index_rows.append(index_row(lesson_dir, prompt_path))

    generated[OUTPUT_ROOT / "README.md"] = build_readme()
    generated[OUTPUT_ROOT / "INDEX.csv"] = build_index(index_rows)

    changed = [path for path, content in generated.items() if read_text(path) != content]
    if args.check:
        if changed:
            print(f"{len(changed)} English visual prompt files need regeneration:")
            for path in changed[:40]:
                print(path.relative_to(REPO_ROOT))
            if len(changed) > 40:
                print(f"... and {len(changed) - 40} more")
            return 1
        print(f"All {len(index_rows)} English lesson prompt packs are current.")
        return 0

    for path in changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(generated[path], encoding="utf-8")

    print(
        f"Generated {len(index_rows)} English lesson prompt packs "
        f"({len(changed)} files changed)."
    )
    return 0


def lesson_dirs() -> list[Path]:
    dirs = [path.parent for path in ENGLISH_ROOT.glob("*/units/*/*/lesson.yaml")]
    return sorted(dirs, key=lesson_sort_key)


def lesson_sort_key(lesson_dir: Path) -> tuple[int, int, int]:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    return (
        LEVEL_ORDER.get(level, 99),
        numeric_prefix(unit_key),
        numeric_prefix(lesson_key),
    )


def lesson_identity(lesson_dir: Path) -> tuple[str, str, str, str]:
    parts = lesson_dir.relative_to(REPO_ROOT / "content" / "curriculum").parts
    return parts[0], parts[1], parts[3], parts[4]


def output_dir(lesson_dir: Path) -> Path:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    return OUTPUT_ROOT / level / unit_key / lesson_key


def build_prompt(lesson_dir: Path) -> str:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    lesson = read_yaml(lesson_dir / "lesson.yaml")
    unit = read_yaml(lesson_dir.parent / "unit.yaml")
    phrases = read_yaml(lesson_dir / "useful_phrases.yaml").get("phrases", [])
    dialogue = dialogue_turns(lesson_dir / "listening_script.md")
    voices = speaker_voices(lesson_dir / "audio_manifest.yaml")
    speakers = unique_speakers(dialogue)
    missing_voices = [speaker for speaker in speakers if speaker not in voices]
    if missing_voices:
        raise ValueError(
            f"Missing audio voice mapping for {', '.join(missing_voices)} in "
            f"{(lesson_dir / 'audio_manifest.yaml').relative_to(REPO_ROOT)}"
        )
    characters = character_profiles(speakers, voices)
    genders = [gender_for_voice(voices.get(speaker, "")) for speaker in speakers]
    situation = extract_section(lesson_dir / "lesson.md", "Situation")
    background = background_spec_for(lesson_dir)
    mode = communication_mode(lesson)
    background_block = background_as_lines(background, mode)
    shared_rules = shared_visual_rules(speakers, genders, characters, mode)
    dialogue_excerpt = "\n".join(
        f"- {speaker}: {text}" for speaker, text in dialogue[: min(6, len(dialogue))]
    )
    unit_number = numeric_prefix(unit_key)
    lesson_number = numeric_prefix(lesson_key)
    target = output_dir(lesson_dir).relative_to(REPO_ROOT)

    hero_prompt = f"""Create a 16:9 hero illustration at 1672×941 pixels for an English lesson.

{shared_rules}

Lesson: {lesson.get('title', lesson_key)} ({level}, Unit {unit_number}, Lesson {lesson_number})
Conversation goal: {lesson.get('conversation_goal', '')}
Situation: {situation}

Scene and background:
{background_block}

Cast and continuity:
{characters_as_lines(characters)}

Show the key conversational moment naturally. The body language, props, and background must make the setting and relationship immediately understandable even without text. Use this dialogue only to understand the action; do not render the words in the image:
{dialogue_excerpt}

Composition: wide establishing shot, all foreground speakers clearly visible, useful negative space, no cropped hands or feet, and no extra foreground characters."""

    card_prompts: list[str] = []
    card_labels: list[str] = []
    for index in range(3):
        phrase = phrase_text(phrases, index, lesson.get("title", lesson_key))
        focus_speaker, focus_line = matching_turn(dialogue, phrase, index)
        card_labels.append(phrase)
        card_prompts.append(
            f"""Create a square companion illustration at 1254×1254 pixels for card {index + 1} of the same English lesson.

{shared_rules}

Use the completed hero image as the visual reference. Keep exactly the same characters, clothing colors, room or location, time of day, and illustration style.

Card focus: “{phrase}”
Conversation moment: {focus_speaker} says “{focus_line}”. Show this meaning through natural gesture, attention, and relevant props; do not render the quote or any other words in the image.
Scene and background:
{background_block}

Cast and continuity:
{characters_as_lines(characters)}

Composition: medium or close conversational shot, clear focus on {focus_speaker}, all needed conversation partners still contextually visible, and no cropped hands."""
        )

    prompt_sections = [
        "# Lesson Visual Prompt",
        "",
        f"- Level: **{level}**",
        f"- Unit {unit_number}: **{unit.get('title', unit_key)}**",
        f"- Lesson {lesson_number}: **{lesson.get('title', lesson_key)}**",
        f"- Lesson key: `{lesson_key}`",
        f"- Web slug: `{lesson.get('slug', '')}`",
        f"- Dialogue speakers: **{', '.join(speakers)}**",
        f"- Prompt folder: `{target}`",
        "",
        "## Suggested outputs",
        "",
        "| File | Size | Purpose |",
        "|---|---:|---|",
        "| `hero.png` | 1672×941 | Main lesson image |",
        f"| `card-1.png` | 1254×1254 | {card_labels[0]} |",
        f"| `card-2.png` | 1254×1254 | {card_labels[1]} |",
        f"| `card-3.png` | 1254×1254 | {card_labels[2]} |",
        "",
        "## Hero prompt",
        "",
        "```text",
        hero_prompt,
        "```",
    ]
    for index, card_prompt in enumerate(card_prompts, start=1):
        prompt_sections.extend(
            [
                "",
                f"## Card {index} prompt — {card_labels[index - 1]}",
                "",
                "```text",
                card_prompt,
                "```",
            ]
        )
    prompt_sections.extend(
        [
            "",
            "Use only the prompts you need. Image generation and asset replacement are intentionally manual.",
            "",
        ]
    )
    return "\n".join(prompt_sections)


def shared_visual_rules(
    speakers: list[str], genders: list[str], characters: list[str], mode: str
) -> str:
    male_count = genders.count("male")
    female_count = genders.count("female")
    remote_scene = "separate appropriate locations" in mode
    if female_count == 0:
        cast_rule = (
            f"MEN-ONLY SCENE. PEOPLE COUNT — show exactly {male_count} adult "
            f"{'man' if male_count == 1 else 'men'} total in the entire image: "
            f"{', '.join(speakers)}. They are the only human figures allowed anywhere. "
            "No women, girls, children, or additional people such as unnamed staff, customers, "
            "travelers, background figures, silhouettes, reflections, portraits, people on screens, "
            "or partial human figures. "
            "Keep every background seat and area empty."
        )
        clothing_rules = (
            "- All depicted people are adult men. They wear modest opaque clothing with loose "
            "trousers whose hems clearly end above the ankle bones, with socks and closed shoes."
        )
        seclusion_rule = ""
    elif male_count == 0:
        cast_rule = (
            f"WOMEN-ONLY SCENE. PEOPLE COUNT — show exactly {female_count} adult "
            f"{'woman' if female_count == 1 else 'women'} total in the entire image: "
            f"{', '.join(speakers)}. They are the only human figures allowed anywhere. "
            "No men, boys, children, or additional people such as unnamed staff, customers, "
            "travelers, background figures, silhouettes, reflections, portraits, people on screens, "
            "or partial human figures. "
            "Keep every background seat and area empty."
        )
        clothing_rules = (
            "- All depicted people are adult women. They wear a long khimar fully covering the "
            "chest, loose opaque full-length clothing, socks, and closed shoes. No hair, neck, "
            "chest, ankles, or feet exposed."
        )
        seclusion_rule = ""
    elif remote_scene:
        cast_rule = (
            f"REMOTE MIXED-GENDER SCENE. PEOPLE COUNT — show exactly {male_count} adult "
            f"{'man' if male_count == 1 else 'men'} and {female_count} adult "
            f"{'woman' if female_count == 1 else 'women'} total across the split image: "
            f"{', '.join(speakers)}. They are physically separate and are the only human figures "
            "allowed anywhere. No additional people, children, staff, customers, background figures, "
            "silhouettes, reflections, portraits, people on screens, or partial human figures."
        )
        clothing_rules = (
            "- Every woman wears a long khimar fully covering the chest, loose opaque full-length "
            "clothing, socks, and closed shoes. No hair, neck, chest, ankles, or feet exposed.\n"
            "- Every man wears modest opaque clothing with loose trousers whose hems clearly end "
            "above the ankle bones, with socks and closed shoes."
        )
        seclusion_rule = f"\n- The mixed-gender speakers are never together physically. {mode}"
    else:
        cast_rule = (
            f"PEOPLE COUNT — show exactly {male_count} adult "
            f"{'man' if male_count == 1 else 'men'} and {female_count} adult "
            f"{'woman' if female_count == 1 else 'women'} as the named foreground speakers: "
            f"{', '.join(speakers)}. Include exactly two additional modestly dressed adult men "
            "as small, distant background figures to make the setting clearly public and prevent "
            "mixed-gender seclusion. No additional women, children, silhouettes, reflections, "
            "portraits, people on screens, or other human figures anywhere."
        )
        clothing_rules = (
            "- Every woman wears a long khimar fully covering the chest, loose opaque full-length "
            "clothing, socks, and closed shoes. No hair, neck, chest, ankles, or feet exposed.\n"
            "- Every man wears modest opaque clothing with loose trousers whose hems clearly end "
            "above the ankle bones, with socks and closed shoes."
        )
        seclusion_rule = f"\n- No private mixed-gender seclusion. {mode}"

    return f"""NON-NEGOTIABLE VISUAL RULES — follow every rule literally:
- {cast_rule}
- FACELESS MEANS COMPLETELY BLANK FACES. Every visible face must be a smooth, unmarked skin-colored shape with zero facial features: no eyes, pupils, eyelids, eyebrows, eyelashes, nose, nostrils, mouth, lips, teeth, ears, beard, moustache, or feature-like dots, lines, shadows, or indentations. This applies equally to the named speakers and every permitted distant background figure. Hair and headwear may frame the blank face shape, but never draw features inside it.
- The named cast must match the dialogue speakers: {', '.join(speakers)}. Do not change their genders, duplicate them, or replace them with generic people.
- Clean editorial illustration with a hand-drawn feel, subtle paper grain, natural proportions, warm daylight, restrained cream/orange/olive/navy palette, and consistent character design.
{clothing_rules}
- Everyone maintains respectful distance; no touching or handshakes.{seclusion_rule}
- No temple, shrine, church, statue, idol, religious building, or religious symbol.
- No readable text, speech bubbles, captions, logos, flags, watermarks, or branded products.
- Avoid glossy 3D rendering, plastic skin, dramatic AI haze, fantasy lighting, distorted anatomy, extra fingers, duplicated limbs, or overly staged poses.
- Before rendering, verify twice: the total human count is exact, no forbidden person appears anywhere, and every face is completely blank."""


def character_profiles(speakers: list[str], voices: dict[str, str]) -> list[str]:
    profiles: list[str] = []
    male_index = 0
    female_index = 0
    for speaker in speakers:
        gender = gender_for_voice(voices.get(speaker, ""))
        if gender == "female":
            clothing = FEMALE_STYLES[female_index % len(FEMALE_STYLES)]
            female_index += 1
            profiles.append(f"{speaker}: adult woman wearing {clothing}")
        else:
            clothing = MALE_STYLES[male_index % len(MALE_STYLES)]
            male_index += 1
            profiles.append(f"{speaker}: adult man wearing {clothing}")
    return profiles


def background_spec_for(lesson_dir: Path) -> BackgroundSpec:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    lesson_key_tuple = (level, unit_key, lesson_key)
    if lesson_key_tuple in LESSON_BACKGROUND_OVERRIDES:
        return LESSON_BACKGROUND_OVERRIDES[lesson_key_tuple]

    unit_key_tuple = (level, unit_key)
    if unit_key_tuple not in UNIT_BACKGROUND_SPECS:
        raise KeyError(
            "Missing reviewed background specification for "
            f"{lesson_dir.relative_to(REPO_ROOT)}"
        )
    return UNIT_BACKGROUND_SPECS[unit_key_tuple]


def background_as_lines(background: BackgroundSpec, mode: str) -> str:
    location, cues, guardrail = background
    return "\n".join(
        [
            f"- Actual conversation location: {location}.",
            f"- Required background cues: {cues}.",
            f"- Context guardrail: {guardrail}",
            f"- Speaker arrangement: {mode}",
        ]
    )


def communication_mode(lesson: dict[str, Any]) -> str:
    situation = str(lesson.get("conversation_situation") or "").lower()
    if situation in REMOTE_SITUATIONS or "by_phone" in situation or "client_call" in situation:
        return (
            "Use a clear split-scene composition: the speakers are in separate appropriate locations connected by phone, not physically together."
        )
    return "The speakers are physically present in the same appropriate scene."


def dialogue_turns(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8").split("## Audio Direction", 1)[0]
    turns: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = re.match(r"^\s*\*\*([^:*#][^:*]{0,40}):\*\*\s*(.+?)\s*$", line)
        if match:
            turns.append((match.group(1).strip(), match.group(2).strip()))
    if not turns:
        raise ValueError(f"No dialogue turns found in {path.relative_to(REPO_ROOT)}")
    return turns


def speaker_voices(path: Path) -> dict[str, str]:
    manifest = read_yaml(path)
    for asset in manifest.get("assets", []):
        mapping = asset.get("speaker_voices") if isinstance(asset, dict) else None
        if isinstance(mapping, dict) and mapping:
            return {str(name): str(voice) for name, voice in mapping.items()}
    raise ValueError(f"No speaker voice mapping found in {path.relative_to(REPO_ROOT)}")


def gender_for_voice(voice: str) -> str:
    normalized = voice.lower()
    return "female" if any(marker in normalized for marker in FEMALE_VOICE_MARKERS) else "male"


def unique_speakers(dialogue: list[tuple[str, str]]) -> list[str]:
    return list(dict.fromkeys(speaker for speaker, _ in dialogue))


def matching_turn(
    dialogue: list[tuple[str, str]], phrase: str, fallback_index: int
) -> tuple[str, str]:
    needle = normalize_phrase(phrase)
    for speaker, line in dialogue:
        haystack = normalize_phrase(line)
        if needle and (needle in haystack or haystack in needle):
            return speaker, line
    return dialogue[min(fallback_index, len(dialogue) - 1)]


def phrase_text(phrases: Any, index: int, fallback: str) -> str:
    if isinstance(phrases, list) and index < len(phrases) and isinstance(phrases[index], dict):
        value = str(phrases[index].get("phrase") or "").strip()
        if value:
            return value
    return fallback


def normalize_phrase(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def extract_section(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    body = text[match.end() :].split("\n##", 1)[0]
    return " ".join(body.strip().split())


def characters_as_lines(characters: list[str]) -> str:
    return "\n".join(f"- {profile}." for profile in characters)


def index_row(lesson_dir: Path, prompt_path: Path) -> dict[str, str]:
    _, level, unit_key, lesson_key = lesson_identity(lesson_dir)
    lesson = read_yaml(lesson_dir / "lesson.yaml")
    return {
        "level": level,
        "unit": f"{numeric_prefix(unit_key):02d}",
        "lesson": f"{numeric_prefix(lesson_key):02d}",
        "lesson_key": lesson_key,
        "slug": str(lesson.get("slug") or ""),
        "title": str(lesson.get("title") or ""),
        "prompt_file": str(prompt_path.relative_to(REPO_ROOT)),
    }


def build_index(rows: list[dict[str, str]]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def build_readme() -> str:
    return """# English lesson visual prompts

This folder contains one production prompt pack for every English lesson. It does not change lesson assets automatically.

Example:

```text
A1/unit-01-greeting-introducing-yourself/lesson-01-saying-hello/
└── PROMPT.md
```

Workflow:

1. Use `INDEX.csv` to find a lesson.
2. Open its `PROMPT.md`.
3. Check the `Scene and background` block: it states the actual conversation location, required visual cues, and context guardrail.
4. Generate only the hero or cards you want to replace.
5. Replace and wire the selected assets manually.

Existing lesson images and visual mappings are intentionally untouched.
"""


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML must contain a mapping: {path.relative_to(REPO_ROOT)}")
    return data


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def numeric_prefix(value: str) -> int:
    match = re.search(r"(?:unit|lesson)-(\d+)", value)
    return int(match.group(1)) if match else 0


if __name__ == "__main__":
    sys.exit(main())
