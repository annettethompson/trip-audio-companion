# Voice Reference

**47 English voices** available in edge-tts, organized by locale and gender.

All voices are free -- no API key, no subscription. They're accessed via Microsoft's Edge browser speech API through the [edge-tts](https://github.com/rany2/edge-tts) library.

## Recommended starting voice

> **`en-GB-RyanNeural`** -- British male, warm documentary quality, excellent for road trip narration. This is the project default.

To preview any voice before committing:

```bash
edge-tts --voice en-GB-RyanNeural --text "Welcome to your road trip audio companion." --write-media preview.mp3
```

To change your voice, edit `config/voice.yaml`:

```yaml
edge_tts:
  voice: en-US-JennyNeural   # replace with any ID below
```

---

## United States (17 voices)

### Male

| Voice ID | Name | Style |
|---|---|---|
| `en-US-AndrewNeural` | Andrew | Warm, confident, authentic -- good for nature narration |
| `en-US-AndrewMultilingualNeural` | Andrew Multilingual | Warm, confident, authentic -- multilingual capable |
| `en-US-BrianNeural` | Brian | Approachable, casual, sincere |
| `en-US-BrianMultilingualNeural` | Brian Multilingual | Approachable, casual, sincere -- multilingual capable |
| `en-US-ChristopherNeural` | Christopher | Reliable, authoritative -- good for history segments |
| `en-US-EricNeural` | Eric | Rational, clear |
| `en-US-GuyNeural` | Guy | Passionate, news-style -- strong for geology and science |
| `en-US-RogerNeural` | Roger | Lively, engaging |
| `en-US-SteffanNeural` | Steffan | Rational, news-novel style |

### Female

| Voice ID | Name | Style |
|---|---|---|
| `en-US-AnaNeural` | Ana (Child) | Cute, conversational -- child persona |
| `en-US-AriaNeural` | Aria | Positive, confident -- news and novel narration |
| `en-US-AvaNeural` | Ava | Expressive, caring, pleasant, friendly |
| `en-US-AvaMultilingualNeural` | Ava Multilingual | Expressive, caring, pleasant -- multilingual capable |
| `en-US-EmmaNeural` | Emma | Cheerful, clear, conversational |
| `en-US-EmmaMultilingualNeural` | Emma Multilingual | Cheerful, clear -- multilingual capable (edge-tts system default) |
| `en-US-JennyNeural` | Jenny | Friendly, considerate, comforting -- excellent all-rounder |
| `en-US-MichelleNeural` | Michelle | Friendly, pleasant -- news and novel style |

---

## United Kingdom (5 voices)

### Male

| Voice ID | Name | Style |
|---|---|---|
| **`en-GB-RyanNeural`** | **Ryan** | **Friendly, documentary-quality -- warm narration style. Project default.** |
| `en-GB-ThomasNeural` | Thomas | Friendly, positive |

### Female

| Voice ID | Name | Style |
|---|---|---|
| `en-GB-LibbyNeural` | Libby | Friendly, positive |
| `en-GB-MaisieNeural` | Maisie (Child) | Friendly, positive -- child persona |
| `en-GB-SoniaNeural` | Sonia | Friendly, positive -- clear and authoritative |

> **Note on Scottish voices:** No dedicated Scottish locale (en-GB-Scottish or similar) exists in edge-tts or the standard Microsoft Azure Neural TTS catalog as of 2026. Microsoft does not publish an en-GB-Scottish or en-SCO locale. The en-GB voices (Ryan, Thomas, Sonia) use standard Received Pronunciation (RP) British English. A Scottish accent is not available through edge-tts without a custom Azure Neural Voice (paid Azure tier, not accessible via this library).

---

## Ireland (2 voices)

| Voice ID | Name | Style |
|---|---|---|
| `en-IE-ConnorNeural` | Connor (Male) | Friendly, positive -- warm storytelling quality |
| `en-IE-EmilyNeural` | Emily (Female) | Friendly, positive -- bright and engaging |

---

## Australia (3 voices)

| Voice ID | Name | Style |
|---|---|---|
| `en-AU-WilliamNeural` | William (Male) | Friendly, positive -- relaxed and approachable |
| `en-AU-WilliamMultilingualNeural` | William Multilingual (Male) | Friendly, positive -- multilingual capable |
| `en-AU-NatashaNeural` | Natasha (Female) | Friendly, positive -- clear and professional |

> The larger en-AU voice set (Annette, Carly, Darren, Duncan, etc.) is Azure Speech SDK only -- not accessible via edge-tts.

---

## Canada (2 voices)

| Voice ID | Name | Style |
|---|---|---|
| `en-CA-LiamNeural` | Liam (Male) | Friendly, positive |
| `en-CA-ClaraNeural` | Clara (Female) | Friendly, positive |

---

## New Zealand (2 voices)

| Voice ID | Name | Style |
|---|---|---|
| `en-NZ-MitchellNeural` | Mitchell (Male) | Friendly, positive |
| `en-NZ-MollyNeural` | Molly (Female) | Friendly, positive |

---

## India (3 voices)

| Voice ID | Name | Style |
|---|---|---|
| `en-IN-PrabhatNeural` | Prabhat (Male) | Friendly, positive |
| `en-IN-NeerjaNeural` | Neerja (Female) | Friendly, positive -- cheerful and empathetic |
| `en-IN-NeerjaExpressiveNeural` | Neerja Expressive (Female) | Friendly, positive -- expressive variant |

---

## South Africa (2 voices)

| Voice ID | Name | Style |
|---|---|---|
| `en-ZA-LukeNeural` | Luke (Male) | Friendly, positive |
| `en-ZA-LeahNeural` | Leah (Female) | Friendly, positive |

---

## Other Locales (12 voices)

| Voice ID | Name | Locale |
|---|---|---|
| `en-HK-SamNeural` | Sam (Male) | Hong Kong |
| `en-HK-YanNeural` | Yan (Female) | Hong Kong |
| `en-SG-WayneNeural` | Wayne (Male) | Singapore |
| `en-SG-LunaNeural` | Luna (Female) | Singapore |
| `en-PH-JamesNeural` | James (Male) | Philippines |
| `en-PH-RosaNeural` | Rosa (Female) | Philippines |
| `en-KE-ChilembaNeural` | Chilemba (Male) | Kenya |
| `en-KE-AsiliaNeural` | Asilia (Female) | Kenya |
| `en-NG-AbeoNeural` | Abeo (Male) | Nigeria |
| `en-NG-EzinneNeural` | Ezinne (Female) | Nigeria |
| `en-TZ-ElimuNeural` | Elimu (Male) | Tanzania |
| `en-TZ-ImaniNeural` | Imani (Female) | Tanzania |

---

## Voice count summary

| Locale | Voices |
|---|---|
| United States (en-US) | 17 |
| United Kingdom (en-GB) | 5 |
| India (en-IN) | 3 |
| Australia (en-AU) | 3 |
| Ireland (en-IE) | 2 |
| Canada (en-CA) | 2 |
| New Zealand (en-NZ) | 2 |
| South Africa (en-ZA) | 2 |
| Hong Kong (en-HK) | 2 |
| Singapore (en-SG) | 2 |
| Philippines (en-PH) | 2 |
| Kenya (en-KE) | 2 |
| Nigeria (en-NG) | 2 |
| Tanzania (en-TZ) | 2 |
| Scotland | 0 (no dedicated locale exists) |
| **Total** | **47** |

Verified: 2026-05-20 by running `python -m edge_tts --list-voices | grep "^en-"`

---

## List voices on your install

Your local edge-tts installation may have slightly different voice availability. To see exactly what you have:

```bash
python -m edge_tts --list-voices | grep "^en-"
```
