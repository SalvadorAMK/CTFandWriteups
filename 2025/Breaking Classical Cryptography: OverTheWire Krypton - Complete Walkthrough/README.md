# Breaking Classical Cryptography: OverTheWire Krypton - Complete Series

A comprehensive walkthrough series breaking all 7 levels of **OverTheWire: Krypton**, from basic encoding to stream ciphers.

## Series Overview

**OverTheWire: Krypton** is a wargame designed to teach cryptanalysis and cipher breaking through hands-on practice. Each level introduces a new cipher with increasing complexity and requires practical attack techniques to defeat it.

**Goal:** Understand how encryption works by learning to break it. Master classical cryptography attacks from simple frequency analysis to advanced statistical methods.

---

## The 7 Levels

### Level 0 → Level 1: Base64
- **Cipher:** Base64 encoding
- **Attack:** Direct decoding with `base64 -d`
- **Key Concept:** Encoding ≠ Encryption (no key required)
- **Time to Break:** Seconds

### Level 1 → Level 2: ROT13
- **Cipher:** Caesar cipher with fixed shift of 13
- **Attack:** Character translation using `tr` command
- **Key Concept:** ROT13 is its own inverse (apply twice = original)
- **Time to Break:** <1 minute

### Level 2 → Level 3: Caesar Cipher
- **Cipher:** Caesar cipher with unknown fixed shift
- **Attack:** Known Plaintext Attack (encrypt the alphabet, observe the shift)
- **Key Concept:** Access to the encryption function reveals the key
- **Time to Break:** 2-5 minutes

### Level 3 → Level 4: Vigenère Cipher 
- **Cipher:** Polyalphabetic substitution with repeating keyword
- **Attack:** Frequency analysis + Trigram detection + Kasiski Examination
- **Key Concept:** Pattern repetition in the key is the cipher's fatal flaw
- **Time to Break:** 15-30 minutes (with scripts)
- **Tools Used:** `freq_analysis.py`, `keyLength.py`, iterative substitution

### Level 4 → Level 5: Vigenère with Longer Key
- **Cipher:** Vigenère with extended key (harder pattern detection)
- **Attack:** Enhanced frequency analysis and multiple ciphertext attack
- **Key Concept:** More key repetitions needed for statistical certainty
- **Time to Break:** 30-45 minutes

### Level 5 → Level 6: XOR Cipher / One-Time Pad Variant
- **Cipher:** Binary XOR operation with repeating key
- **Attack:** Frequency analysis on XOR'd data + multi-text correlation
- **Key Concept:** XOR is fast but still vulnerable to frequency analysis when key repeats
- **Time to Break:** 45-60 minutes

### Level 6 → Level 7: Stream Cipher
- **Cipher:** Pseudo-random stream cipher
- **Attack:** State machine analysis + cryptanalytic techniques specific to stream ciphers
- **Key Concept:** PRNG weaknesses and synchronization attacks
- **Time to Break:** 60+ minutes (requires deeper cryptanalysis)

---

## Attack Methodology Chain

```
Base64          → Decode directly
                ↓
ROT13           → Shift by 13 / brute force 26 shifts
                ↓
Caesar          → Known Plaintext Attack
                ↓
Vigenère        → Frequency Analysis + Trigram Detection
                ↓
Extended Vig.   → Multi-text Frequency Analysis
                ↓
XOR Cipher      → Frequency Analysis on Binary + Brute Force
                ↓
Stream Cipher   → State Analysis + Cryptanalytic Attacks
```

---

## Part 1: Levels 0-3 Complete Walkthrough

**File:** `part1/krypton_writeup_part1.md`

Covers detailed step-by-step solutions for:
- Base64 encoding and decoding
- ROT13 cipher breaking
- Caesar cipher with known plaintext attack
- Vigenère cipher with multiple ciphertexts
- Complete Python scripts for cryptanalysis

### Scripts Included in Part 1

1. **freq_analysis.py** - Count character and n-gram frequencies
   - Usage: `python3 freq_analysis.py <file> <groupsize>`
   - Identifies most common letters, bigrams, trigrams

2. **keyLength.py** - Kasiski Examination implementation
   - Estimates Vigenère key length from repeated sequences
   - Calculates GCD of inter-sequence distances

3. **vignere_shift.py** - Column extractor for polyalphabetic ciphers
   - Isolates characters encrypted by same key byte
   - Turns Vigenère into multiple Caesar ciphers

4. **vignere_decoder.py** - Decryption with known key
   - Formula: `plaintext[i] = (ciphertext[i] - key[i % keylen]) mod 26`

---

## Key Concepts Across All Levels

| Concept | Relevant Levels | Why It Matters |
|---------|-----------------|----------------|
| **Frequency Analysis** | 1-7 | Most common letters reveal plaintext patterns |
| **N-gram Analysis** | 3-7 | Repeated sequences like "THE" expose patterns |
| **Known Plaintext Attack** | 2-7 | Access to encryption reveals the transformation |
| **Brute Force** | 0-5 | Limited keyspace makes exhaustive search viable |
| **Statistical Deviation** | 3-7 | Ciphertexts deviate from English distributions |
| **Kasiski Examination** | 3-5 | Repeating keys leave measurable traces |
| **XOR Properties** | 5-6 | XOR with same key multiple times leaks information |

---

## Common Attack Patterns

### Pattern 1: Single Character Dominates
When one letter appears far more frequently than others, it likely maps to **E** (most common in English).

### Pattern 2: Repeating N-grams
The same ciphertext sequence appearing multiple times suggests either:
- A repeating key of length = distance between repetitions
- A common English word like "THE"

### Pattern 3: Frequency Distribution Flattening
When all letters appear with roughly equal frequency, the cipher is using:
- Polyalphabetic substitution (like Vigenère)
- XOR with different key bytes per position
- Solution: Extract individual columns and apply monoalphabetic analysis to each

### Pattern 4: Correlation Across Multiple Texts
When multiple ciphertexts encrypted with the same key show correlated statistics:
- Combine them for stronger frequency analysis
- Find common patterns across all texts
- Use as "side channels" to recover the key

---

## Tools & Environment

**Required:**
- Linux/Unix terminal
- Python 3.x
- Standard Unix utilities: `tr`, `echo`, `cat`, `ssh`, `scp`

**Optional but Recommended:**
- `ghidra` or similar for Level 6-7 if binary analysis needed
- Frequency analysis tools (included scripts)
- Text analysis tools: `grep`, `sort`, `uniq`

---

## Progression Timeline

| Level | Cipher Type | Complexity | Estimated Time | Key Skill |
|-------|-------------|-----------|-----------------|-----------|
| 0-1 | Encoding + Simple Shift | Trivial | <5 min | Pattern Recognition |
| 2 | Fixed Shift | Easy | 5-10 min | Known Plaintext |
| 3-4 | Repeating Key | Medium | 30-45 min | Frequency Analysis |
| 5 | XOR / Binary | Medium-Hard | 45-60 min | Binary Analysis |
| 6-7 | Stream / Complex | Hard | 60+ min | Cryptanalysis |

---

## Master Principle

**Every cipher leaks information through patterns.** Your job is to:
1. **Identify the pattern** (character frequency, repeating sequences, statistical deviation)
2. **Exploit the pattern** (frequency analysis, known plaintext, brute force)
3. **Recover the key or plaintext** (reconstruct the transformation)

As ciphers increase in complexity, the patterns become more subtle and require more sophisticated analysis-but the principle remains constant.

---

## References

- **OverTheWire: Krypton** - https://overthewire.org/wargames/krypton/
- **Frequency Analysis** - Classical cryptanalysis technique
- **Kasiski Examination** - Method to find repeating key length
- **Vigenère Cipher** - Polyalphabetic cipher (1553)

---

**Author:** Abdelrahman Mohamed  
**Series Status:** 
- Part 1 (Levels 0-3):  Complete
- Part 2 (Levels 4-5):
- Part 3 (Levels 6-7):

