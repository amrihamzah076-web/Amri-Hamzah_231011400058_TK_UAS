# Tugas Proyek Akhir: Representasi Tahapan Kompilasi

**Oleh:** Amri Hamzah  
**Mata Kuliah:** Teknik Kompilasi

---

## 1. Pilihan Konstruksi
Konstruksi sintaksis yang dipilih untuk diimplementasikan adalah **Perulangan (Looping: While)**.
Bentuk umum perulangan ini mengevaluasi sebuah kondisi di awal; jika kondisi bernilai `True` (benar), maka blok pernyataan (statement) di dalamnya akan dieksekusi terus-menerus hingga kondisi bernilai `False`.

---

## 2. Pattern (Pola Sintaks)
Pola tata bahasa didefinisikan menggunakan pendekatan *Backus-Naur Form* (BNF) sederhana:

```bnf
<while_stmt> ::= "while" "(" <condition> ")" "{" <statements> "}"
<condition>  ::= <identifier> <operator> <value>
<operator>   ::= "<" | ">" | "==" | "!=" | "<=" | ">="
<statements> ::= <identifier> "=" <expression> ";"
<expression> ::= <identifier> | <value> | <identifier> <arithmetic_op> <value>

3. Implementasi Program
Berikut adalah simulasi compiler pipeline menggunakan bahasa pemrograman Python. Program ini memodelkan keempat tahapan secara terstruktur: memecah token, membentuk Abstract Syntax Tree (AST) sederhana, memvalidasi semantik melalui symbol table tiruan, dan merakitnya menjadi bentuk TAC.
