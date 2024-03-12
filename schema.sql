CREATE TABLE "pokemonkarten" (
  "id"	INTEGER NOT NULL UNIQUE,
  "Name"	TEXT NOT NULL,
  "Typ"		TEXT,
  "Serie"	TEXT,
  "Entwicklung"	TEXT,
  "KP"		INTEGER,
  "Seltenheit"	TEXT,
  "Holo"	TEXT,
  "Special"	TEXT,
  "Schwaeche"	TEXT,
  "Resistenz"	TEXT,
  "Anzahl"	INTEGER,
  "Sprache"	TEXT,
  "Decks"	TEXT,
  PRIMARY KEY("id" AUTOINCREMENT)
)
