# Spécifications Techniques et Fonctionnelles (STF)

## Skill Interactif "Vibe-Coding" & Mentor Dev

## 1. Vision et Objectifs

### 1.1 Contexte

Des profils non-techniciens ou "vibe codeurs" utilisent massivement des assistants IA pour générer du code. Cette pratique sans garde-fous entraîne une dette technique immédiate : prolifération de code dupliqué, fichiers monolithes, modifications manuelles par IA de fichiers volumineux (au lieu d'automatisation déterministe) et absence d'architecture maintenable.

### 1.2 Objectif du produit

Créer un **Skill Interactif (Mentor/Coach)** utilisable aussi bien en **CLI** (ligne de commande) qu'en **Interface Web** (chat/UI). Ce skill a pour vocation :

1. De **former** les non-techniciens aux règles fondamentales d'un développement maintenable (Mode Initiation).

2. D'**auditer** les projets existants pour identifier les dérives architecturales (Mode Audit).

3. D'**intercepter et guider** les requêtes de génération de code pour empêcher la casse en temps réel (Mode Mentor).

## 2. Principes Fondamentaux & Discipline Équipe

Pour garantir la pérennité des projets, le skill impose 4 principes non-négociables :

### 2.1 Pas de développement dans les chats !
* **Règle :** Le chat d'une IA ne sert qu'à la réflexion, la conception, le débogage et l'explication.
* **Application :** Tout code doit vivre dans un vrai dépôt de code, édité via un IDE/éditeur approprié ou manipulé via des scripts dédiés. Il est strictement interdit d'utiliser un fil de discussion LLM comme espace d'exécution ou de stockage de code.

### 2.2 Gestion de version obligatoire (Git & Forge Git)
* **Règle :** Aucun code ou script ne doit exister hors d'un suivi de version Git connecté à la forge officielle de l'organisation (GitHub / GitLab / Bitbucket d'entreprise).
* **Application :** Le skill vérifie la présence d'un dépôt Git initialisé et branché sur le remote officiel avant de valider toute modification ou génération.

### 2.3 Respect du Référentiel Technique (Tech Stack)
L'IA et l'utilisateur doivent strictement respecter la stack technique selon la nature du besoin :
* **Scripts & Outillage d'automatisation :** `Python` (ou scripts Shell encadrés).
* **Applications web / services en ligne :** `Node.js` / `TypeScript`.
* **Applications lourdes / performances critiques :** `Rust`.
*(Note : Ce référentiel est configurable selon la charte technique de l'organisation).*

### 2.4 Tailles de fichiers raisonnables
* La limite stricte est ajustée pour éviter la sur-fragmentation inutile tout en empêchant les monolithes. Un fichier ne doit idéalement pas dépasser **400 à 500 lignes** de code actif (hors commentaires/imports majeurs). Au-delà, un découpage modulaire devient obligatoire.

---

## 3. Modes de Fonctionnement

Le skill s'articule autour de 3 modes principaux.

```
+-------------------------------------------------------------------+
|                        SKILL INTERACTIF                           |
+-------------------------+------------------+----------------------+
                          |                  |
                          v                  v
+---------------------------+  +---------------------------+  +---------------------------+
|    1. MODE INITIATION     |  |     2. MODE AUDIT         |  |     3. MODE MENTOR        |
|  (Sandbox & Katas)        |  |  (Analyse d'existant)     |  |  (Garde-fou temps réel)   |
+---------------------------+  +---------------------------+  +---------------------------+
| - Atelier 1: Script vs IA |  | - Scan de métriques       |  | - Interception de prompt  |
| - Atelier 2: Découpe UI   |  | - Rapport de dette        |  | - Validation étape par    |
| - Atelier 3: Anti-doublons|  | - Plan de refactoring     |  |   étape (Gatekeeper)      |
+---------------------------+  +---------------------------+  +---------------------------+
```

### 3.1 Mode 1 : Initiation / Onboarding (Sandbox)

Le Mode Initiation est un parcours pratique composé de 3 ateliers sous forme de **Code Katas**. Il s'exécute dans un environnement isolé (`.sandbox/` ou dépôt temporaire Git) sans risquer d'altérer le code de production.

#### Atelier 1 : "IA vs Script" (Automatisation & Déterminisme en Python)
* **Mise en situation :** Un dossier contient 50 fichiers JSON de configuration mal formatés.
* **Comportement attendu du vibe codeur :** *"Demander à l'IA dans le chat de corriger les 50 fichiers un par un."*
* **Intervention du Skill :**
  1. Bloque la demande directe dans le chat.
  2. Explique le risque (hallucination, lenteur, non-déterminisme, coût en tokens).
  3. Guide l'utilisateur dans l'écriture d'un script `Python` réutilisable.
  4. Fait commiter le script sur Git et l'exécute via le CLI pour constater le résultat immédiat.

#### Atelier 2 : "La Découpe & La Stack" (Architecture & Modularité)
* **Mise en situation :** Un fichier monolithique dépassant les 500 lignes de code mélangé.
* **Intervention du Skill :**
  1. Guide le découpage pas à pas selon le référentiel technique (ex: séparation de la logique Node.js et de l'UI).
  2. Démontre qu'une structure modulaire permet à l'IA de générer des réponses 10x plus précises et fiables par la suite.

#### Atelier 3 : "La Chasse aux Doublons & Git workflow" (Connaissance de l'Existant)
* **Mise en situation :** Un projet où 3 fonctions similaires existent sous des noms différents.
* **Intervention du Skill :**
  1. Enseigne le réflexe de recherche (Grep/AST) dans le dépôt Git *avant* d'exiger une nouvelle fonction à l'IA.
  2. Enseigne la création d'une branche Git dédiée pour toute nouvelle fonctionnalité.

### 3.2 Mode 2 : Audit & Diagnostic (Sur code existant)

Ce mode est déclenché sur un dépôt Git existant pour dresser un état des lieux de la santé du code.

* **Indicateurs clés analysés :**
  * **Conformité au Référentiel Technique :** Vérification du respect des langages attribués (Python pour scripts, Node.js pour le web, Rust pour le lourd).
  * **Présence & Bon usage de Git :** Détection du dépôt distant officiel (GitHub/GitLab d'entreprise), commits atomiques vs commits géants.
  * **Taille des fichiers :** Détection des fichiers dépassant le seuil critique (500+ lignes).
  * **Taux de duplication :** Détection des fonctions quasi-identiques.
  * **Absence de scripts d'automatisation :** Présence de tâches manuelles répétées dans l'historique.

* **Livrables de l'audit :**
  * Un rapport synthétique Markdown (Score global, Top 5 des priorités de refactoring).
  * Un plan d'action étape par étape sous forme d'Issues GitHub/GitLab à traiter.

### 3.3 Mode 3 : Mentor & Garde-fou (Temps réel)

C'est le mode par défaut en cours de travail. Il agit comme un **gatekeeper**.

* **Règles d'interception :**
  1. **Interdiction du "Dev in Chat" :** Si l'utilisateur demande d'écrire un projet complet dans le chat, le skill exige la sélection d'un dossier local Git-initialisé.
  2. **Contrôle de la Stack :** Refuse de générer du code dans un langage non-conforme au référentiel du projet (ex: interdiction d'un script d'outillage en Bash complexe si la règle est Python).
  3. **Limite de taille de fichier :** Alerte dès qu'un fichier approche des 400 lignes et bloque la génération si la barre des 500 lignes est dépassée, imposant une refactorisation.
  4. **Interdiction de modification massive directe :** Si la demande concerne plus de 5 fichiers de données, force la création d'un script Python.

---

## 4. Architecture Technique et Intégrations

### 4.1 Compatibilité Multi-Interface

```
+-----------------------------------------------------------------------------------+
|                                  CORE LOGIC                                       |
|    (Prompts Système, Checkers Git/Stack, Moteur AST, Rules Engine & Validation)   |
+----------------------------------------+------------------------------------------+
                                         |
                   +---------------------+---------------------+
                   |                                           |
                   v                                           v
+-------------------------------------+     +-------------------------------------+
|              CLI TOOL               |     |            WEB INTERFACE            |
| (Node.js/Bun CLI, Shell Exec, Git)  |     |   (React Immersive, Monaco Editor)  |
+-------------------------------------+     +-------------------------------------+
```

1. **Interface CLI :**
   * Vérifie la configuration Git locale (`git remote -v`, état de la branche).
   * Interagit directement avec le système de fichiers pour lancer l'outillage et les tests.

2. **Interface Web :**
   * Visualisation interactive de l'arbre Git, rapport d'audit et validation des étapes d'initiation.

---

## 5. Prompt Système Central (Spécification de l'Agent)

```
RÔLE : Tu es un Lead Developer et Mentor Pédagogique ultra-exigeant mais bienveillant. 
MISSION : Empêcher le "vibe coding" destructeur et imposer les meilleures pratiques d'ingénierie logicielle.

REGLES ABSOLUES ET NON-NÉGOCIABLES :
1. LE CHAT N'EST PAS UN EDITEUR DE CODE. Tout code doit être destiné à être versionné sous Git dans la forge d'entreprise (GitHub/GitLab).
2. RESPECT DU RÉFÉRENTIEL TECHNIQUE :
   - Scripts & Automation = Python
   - Services & Applications Web = Node.js / TypeScript
   - Performance / App Lourde = Rust
3. PAS DE FICHIERS MONSTRES : Bloquer toute génération dans un fichier dépassant 500 lignes. Exiger une découpe modulaire dès 400 lignes.
4. JAMAIS DE TRAITEMENT MASSIF PAR IA : Si plus de 5 fichiers de données/config doivent être modifiés, forcer la création et l'exécution d'un script Python déterministe.
5. EXIGER UN COMMIT ET UNE BRANCHE GIT pour chaque étape franchie.
```

## 6. Critères d'Acceptation et Succès

* **Critère 1 (Discipline Git) :** 100% du code généré ou modifié réside dans un dépôt Git synchronisé avec la forge officielle.
* **Critère 2 (Conformité Stack) :** Les scripts d'outillage sont tous écrits en Python, le web en Node.js/TS, et les composants critiques en Rust.
* **Critère 3 (Pas de monolithisme) :** Aucun fichier du projet ne dépasse 500 lignes.
* **Critère 4 (Autonomie Outillage) :** Les utilisateurs créent et exécutent des scripts Python d'automatisation au lieu d'utiliser le chat IA comme moulin à texte.