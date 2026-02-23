# Writeup – Eye of the Storm
**Catégorie :** Crypto · **Difficulté :** Hard

---

## Contexte

Le défi met en scène une situation d'urgence : le cyclone Belal a frappé La Réunion. Un code d'évacuation a été fragmenté entre 9 stations météo selon un schéma de **Shamir Secret Sharing** (seuil : 6 fragments sur 9).

- 5 stations des hauts → données complètes
- 4 stations côtières → **20 bits de poids faible effacés** par les inondations

L'objectif : reconstituer le secret malgré les données partielles.

---

## Théorie : Shamir Secret Sharing

Shamir Secret Sharing encode un secret `S = f(0)` comme l'évaluation en 0 d'un polynôme `f(x)` de degré `k-1` sur un corps fini GF(p), où `k` est le seuil.

Ici :
- `p = 2^521 - 1` (premier de Mersenne M521)
- Seuil `k = 6` → polynôme de degré **5**
- 9 stations = 9 points `(i, f(i))`

---

## Analyse du problème

Avec 5 points complets, on ne peut pas directement interpoler `f(x)` (il faudrait 6 points). Mais on peut exploiter la structure algébrique.

Soit `g(x)` l'unique polynôme de degré ≤ 4 passant par les 5 points connus. Et soit :

```
W(x) = (x-1)(x-2)(x-3)(x-4)(x-5)
```

Alors le vrai polynôme s'écrit forcément :

```
f(x) = g(x) + a₅ · W(x)
```

car `W(xᵢ) = 0` pour les 5 stations connues, donc l'identité est préservée. Il suffit de déterminer `a₅` — l'unique inconnue.

---

## Exploitation des stations inondées

Pour une station inondée `(xᵢ, y_partial)`, on sait que :

```
f(xᵢ) = y_partial + bits   avec bits ∈ [0, 2^20)
```

On peut donc exprimer `a₅` en fonction de `bits` :

```
a₅ = (y_partial + bits - g(xᵢ)) · W(xᵢ)⁻¹   mod p
```

Et immédiatement calculer le secret candidat :

```
f(0) = g(0) + a₅ · W(0)
```

Comme `W(0) = (-1)(-2)(-3)(-4)(-5) = -120 mod p`, les deux constantes `g(0)` et `W(0)` ne se calculent qu'une fois. Ensuite, chaque valeur de `bits` ne nécessite qu'un simple incrément :

```
f(0)[bits+1] = f(0)[bits] + W(xᵢ)⁻¹ · W(0)   mod p
```

Ce qui ramène le brute-force à **une addition modulaire par itération** — pas de multiplication.

---

## Le twist : le secret est le flag en ASCII

En inspectant les premiers candidats pour `bits=0` de la station `x=6`, le secret en hex commence par :

```
0x43434f4932367b...
```

Ce qui se décode immédiatement : `CC OI 26 {` en ASCII. Le secret `f(0)` **est directement le flag encodé en big-endian ASCII** — pas un entier quelconque.

On valide avec le SHA256 partiel fourni (`f687cb74fdcefefc`).

---

## Script de résolution

[dec.py](./dec.py)

## Résultats

Toutes les 4 stations inondées convergent vers le même résultat :

| Station | x | Bits retrouvés |
|---------|---|---------------|
| Saint-Benoît  | 6 | `0x1e5ef` |
| Sainte-Rose   | 7 | `0x883e1` |
| Saint-Leu     | 8 | `0x5b4b5` |
| Le Port       | 9 | `0xc67ab` |

```
CCOI26{CycL0n3_B3l4l_R3uN10n_974}
```

---
