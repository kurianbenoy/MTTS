## Introduction [to TTS](https://www.academia.edu/416871/A_Short_Introduction_to_Text-to-Speech_Synthesis)



This section runs through the definition of a new voice in Festival. Although this voice is simple (it is a simplified version of the distributed spanish voice) it shows all the major parts that must be defined to get Festival to speak in a new voice. Thanks go to Alistair Conkie for helping me define this but as I don't speak Spanish there are probably many mistakes. Hopefully its pedagogical use is better than its ability to be understood in Castille.

A much more detailed document on building voices in Festival has been written and is recommend reading for any one attempting to add a new voice to Festival black99. The information here is a little sparse though gives the basic requirements.

The general method for defining a new voice is to define the parameters for all the various sub-parts e.g. phoneset, duration parameter intonation parameters etc., then defined a function of the form voice_NAME which when called will actually select the voice.

## 24.2.1 Phoneset

For most new languages and often for new dialects, a new phoneset is required. It is really the basic building block of a voice and most other parts are defined in terms of this set, so defining it first is a good start.

(defPhoneSet
  spanish
  ;;;  Phone Features
  (;; vowel or consonant
   (vc + -)  
   ;; vowel length: short long diphthong schwa
   (vlng s l d a 0)
   ;; vowel height: high mid low
   (vheight 1 2 3 -)
   ;; vowel frontness: front mid back
   (vfront 1 2 3 -)
   ;; lip rounding
   (vrnd + -)
   ;; consonant type: stop fricative affricative nasal liquid
   (ctype s f a n l 0)
   ;; place of articulation: labial alveolar palatal labio-dental
   ;;                         dental velar
   (cplace l a p b d v 0)
   ;; consonant voicing
   (cvox + -)
   )
  ;; Phone set members (features are not! set properly)
  (
   (#  - 0 - - - 0 0 -)
   (a  + l 3 1 - 0 0 -)
   (e  + l 2 1 - 0 0 -)
   (i  + l 1 1 - 0 0 -)
   (o  + l 3 3 - 0 0 -)
   (u  + l 1 3 + 0 0 -)
   (b  - 0 - - + s l +)
   (ch - 0 - - + a a -)
   (d  - 0 - - + s a +)
   (f  - 0 - - + f b -)
   (g  - 0 - - + s p +)
   (j  - 0 - - + l a +)
   (k  - 0 - - + s p -)
   (l  - 0 - - + l d +)
   (ll - 0 - - + l d +)
   (m  - 0 - - + n l +)
   (n  - 0 - - + n d +)
   (ny - 0 - - + n v +)
   (p  - 0 - - + s l -)
   (r  - 0 - - + l p +)
   (rr - 0 - - + l p +)
   (s  - 0 - - + f a +)
   (t  - 0 - - + s t +)
   (th - 0 - - + f d +)
   (x  - 0 - - + a a -)
  )
)
(PhoneSet.silences '(#))

Note some phonetic features may be wrong.

## 24.2.2 Lexicon and LTS

Spanish is a language whose pronunciation can almost completely be predicted from its orthography so in this case we do not need a list of words and their pronunciations and can do most of the work with letter to sound rules.

Let us first make a lexicon structure as follows

(lex.create "spanish")
(lex.set.phoneset "spanish")

However if we did just want a few entries to test our system without building any letter to sound rules we could add entries directly to the addenda. For example

(lex.add.entry
   '("amigos" nil (((a) 0) ((m i) 1) (g o s))))

A letter to sound rule system for Spanish is quite simple in the format supported by Festival. The following is a good start to a full set.

(lts.ruleset
;  Name of rule set
 spanish
;  Sets used in the rules
(
  (LNS l n s )
  (AEOU a e o u )
  (AEO a e o )
  (EI e i )
  (BDGLMN b d g l m n )
)
;  Rules
(
 ( [ a ] = a )
 ( [ e ] = e )
 ( [ i ] = i )
 ( [ o ] = o )
 ( [ u ] = u )
 ( [ "'" a ] = a1 )   ;; stressed vowels
 ( [ "'" e ] = e1 )
 ( [ "'" i ] = i1 )
 ( [ "'" o ] = o1 )
 ( [ "'" u ] = u1 )
 ( [ b ] = b )
 ( [ v ] = b )
 ( [ c ] "'" EI = th )
 ( [ c ] EI = th )
 ( [ c h ] = ch )
 ( [ c ] = k )
 ( [ d ] = d )
 ( [ f ] = f )
 ( [ g ] "'" EI = x )
 ( [ g ] EI = x )
 ( [ g u ] "'" EI = g )
 ( [ g u ] EI = g )
 ( [ g ] = g )
 ( [ h u e ] = u e )
 ( [ h i e ] = i e )
 ( [ h ] =  )
 ( [ j ] = x )
 ( [ k ] = k )
 ( [ l l ] # = l )
 ( [ l l ] = ll )
 ( [ l ] = l )
 ( [ m ] = m )
 ( [ ~ n ] = ny )
 ( [ n ] = n )
 ( [ p ] = p )
 ( [ q u ] = k )
 ( [ r r ] = rr )
 ( # [ r ] = rr )
 ( LNS [ r ] = rr )
 ( [ r ] = r )
 ( [ s ] BDGLMN = th )
 ( [ s ] = s )
 ( # [ s ] C = e s )
 ( [ t ] = t )
 ( [ w ] = u )
 ( [ x ] = k s )
 ( AEO [ y ] = i )
 ( # [ y ] # = i )
 ( [ y ] = ll )
 ( [ z ] = th )
))

We could simply set our lexicon to use the above letter to sound system with the following command

(lex.set.lts.ruleset 'spanish)

But this would not deal with upper case letters. Instead of writing new rules for upper case letters we can define that a Lisp function be called when looking up a word and intercept the lookup with our own function. First we state that unknown words should call a function, and then define the function we wish called. The actual link to ensure our function will be called is done below at lexicon selection time

(define (spanish_lts word features)
  "(spanish_lts WORD FEATURES)
Using letter to sound rules build a spanish pronunciation of WORD."
  (list word
        nil
        (lex.syllabify.phstress (lts.apply (downcase word) 'spanish))))
(lex.set.lts.method spanish_lts)

In the function we downcase the word and apply the LTS rule to it. Next we syllabify it and return the created lexical entry.

## 24.2.3 Phrasing

Without detailed labelled databases we cannot build statistical models of phrase breaks, but we can simply build a phrase break model based on punctuation. The following is a CART tree to predict simple breaks, from punctuation.

(set! spanish_phrase_cart_tree
'
((lisp_token_end_punc in ("?" "." ":"))
  ((BB))
  ((lisp_token_end_punc in ("'" "\"" "," ";"))
   ((B))
   ((n.name is 0)  ;; end of utterance
    ((BB))
    ((NB))))))

## 24.2.4 Intonation

For intonation there are number of simple options without requiring training data. For this example we will simply use a hat pattern on all stressed syllables in content words and on single syllable content words. (i.e. Simple) Thus we need an accent prediction CART tree.

(set! spanish_accent_cart_tree
 '
  ((R:SylStructure.parent.gpos is content)
   ((stress is 1)
    ((Accented))
    ((position_type is single)
     ((Accented))
     ((NONE))))
   ((NONE))))

We also need to specify the pitch range of our speaker. We will be using a male Spanish diphone database of the follow range

(set! spanish_el_int_simple_params
    '((f0_mean 120) (f0_std 30)))

## 24.2.5 Duration

We will use the trick mentioned above for duration prediction. Using the zscore CART tree method, we will actually use it to predict factors rather than zscores.

The tree predicts longer durations in stressed syllables and in clause initial and clause final syllables.

(set! spanish_dur_tree
 '
   ((R:SylStructure.parent.R:Syllable.p.syl_break > 1 ) ;; clause initial
    ((R:SylStructure.parent.stress is 1)
     ((1.5))
     ((1.2)))
    ((R:SylStructure.parent.syl_break > 1)   ;; clause final
     ((R:SylStructure.parent.stress is 1)
      ((2.0))
      ((1.5)))
     ((R:SylStructure.parent.stress is 1)
      ((1.2))
      ((1.0))))))

In addition to the tree we need durations for each phone in the set

(set! spanish_el_phone_data
'(
   (# 0.0 0.250)
   (a 0.0 0.090)
   (e 0.0 0.090)
   (i 0.0 0.080)
   (o 0.0 0.090)
   (u 0.0 0.080)
   (b 0.0 0.065)
   (ch 0.0 0.135)
   (d 0.0 0.060)
   (f 0.0 0.100)
   (g 0.0 0.080)
   (j 0.0 0.100)
   (k 0.0 0.100)
   (l 0.0 0.080)
   (ll 0.0 0.105)
   (m 0.0 0.070)
   (n 0.0 0.080)
   (ny 0.0 0.110)
   (p 0.0 0.100)
   (r 0.0 0.030)
   (rr 0.0 0.080)
   (s 0.0 0.110)
   (t 0.0 0.085)
   (th 0.0 0.100)
   (x 0.0 0.130)
))

24.2.6 Waveform synthesis

There are a number of choices for waveform synthesis currently supported. MBROLA supports Spanish, so we could use that. But their Spanish diphones in fact use a slightly different phoneset so we would need to change the above definitions to use it effectively. Here we will use a diphone database for Spanish recorded by Eduardo Lopez when he was a Masters student some years ago.

Here we simply load our pre-built diphone database

(us_diphone_init
   (list
    '(name "el_lpc_group")
    (list 'index_file 
          (path-append spanish_el_dir "group/ellpc11k.group"))
    '(grouped "true")
    '(default_diphone "#-#")))

## 24.2.7 Voice selection function

The standard way to define a voice in Festival is to define a function of the form voice_NAME which selects all the appropriate parameters. Because the definition below follows the above definitions we know that everything appropriate has been loaded into Festival and hence we just need to select the appropriate a parameters.

(define (voice_spanish_el)
"(voice_spanish_el)
Set up synthesis for Male Spanish speaker: Eduardo Lopez"
  (voice_reset)
  (Parameter.set 'Language 'spanish)  
  ;; Phone set
  (Parameter.set 'PhoneSet 'spanish)
  (PhoneSet.select 'spanish)
  (set! pos_lex_name nil)
  ;; Phrase break prediction by punctuation
  (set! pos_supported nil)
  ;; Phrasing
  (set! phrase_cart_tree spanish_phrase_cart_tree)
  (Parameter.set 'Phrase_Method 'cart_tree)
  ;; Lexicon selection
  (lex.select "spanish")
  ;; Accent prediction
  (set! int_accent_cart_tree spanish_accent_cart_tree)
  (set! int_simple_params spanish_el_int_simple_params)
  (Parameter.set 'Int_Method 'Simple)
  ;; Duration prediction
  (set! duration_cart_tree spanish_dur_tree)
  (set! duration_ph_info spanish_el_phone_data)
  (Parameter.set 'Duration_Method 'Tree_ZScores)
  ;; Waveform synthesizer: diphones
  (Parameter.set 'Synth_Method 'UniSyn)
  (Parameter.set 'us_sigpr 'lpc)
  (us_db_select 'el_lpc_group)

  (set! current-voice 'spanish_el)
)

(provide 'spanish_el)

## 24.2.8 Last remarks

We save the above definitions in a file `spanish_el.scm'. Now we can declare the new voice to Festival. See section 24.3 Defining a new voice for a description of methods for adding new voices. For testing purposes we can explciitly load the file `spanish_el.scm'

The voice is now available for use in festival.

festival> (voice_spanish_el)
spanish_el
festival> (SayText "hola amigos")
<Utterance 0x04666>

As you can see adding a new voice is not very difficult. Of course there is quite a lot more than the above to add a high quality robust voice to Festival. But as we can see many of the basic tools that we wish to use already exist. The main difference between the above voice and the English voices already in Festival are that their models are better trained from databases. This produces, in general, better results, but the concepts behind them are basically the same. All of those trainable methods may be parameterized with data for new voices.

As Festival develops, more modules will be added with better support for training new voices so in the end we hope that adding in high quality new voices is actually as simple as (or indeed simpler than) the above description.
24.2.9 Resetting globals

Because the version of Scheme used in Festival only has a single flat name space it is unfortunately too easy for voices to set some global which accidentally affects all other voices selected after it. Because of this problem we have introduced a convention to try to minimise the possibility of this becoming a problem. Each voice function defined should always call voice_reset at the start. This will reset any globals and also call a tidy up function provided by the previous voice function.

Likewise in your new voice function you should provide a tidy up function to reset any non-standard global variables you set. The function current_voice_reset will be called by voice_reset. If the value of current_voice_reset is nil then it is not called. voice_reset sets current_voice_reset to nil, after calling it.

For example suppose some new voice requires the audio device to be directed to a different machine. In this example we make the giant's voice go through the netaudio machine big_speakers while the standard voice go through small_speakers.

Although we can easily select the machine big_speakers as out when our voice_giant is called, we also need to set it back when the next voice is selected, and don't want to have to modify every other voice defined in the system. Let us first define two functions to selection the audio output.

(define (select_big)
  (set! giant_previous_audio (getenv "AUDIOSERVER"))
  (setenv "AUDIOSERVER" "big_speakers"))

(define (select_normal)
  (setenv "AUDIOSERVER" giant_previous_audio))

Note we save the previous value of AUDIOSERVER rather than simply assuming it was small_speakers.

Our definition of voice_giant definition of voice_giant will look something like

(define (voice_giant)
"comment comment ..."
   (voice_reset)  ;; get into a known state
   (select_big)
   ;;; other giant voice parameters
   ...

   (set! current_voice_rest select_normal)
   (set! current-voice 'giant))

The obvious question is which variables should a voice reset. Unfortunately there is not a definitive answer to that. To a certain extent I don't want to define that list as there will be many variables that will by various people in Festival which are not in the original distribution and we don't want to restrict them. The longer term answer is some for of partitioning of the Scheme name space perhaps having voice local variables (cf. Emacs buffer local variables). But ultimately a voice may set global variables which could redefine the operation of later selected voices and there seems no real way to stop that, and keep the generality of the system.

Note the convention of setting the global current-voice as the end of any voice definition file. We do not enforce this but probabaly should. The variable current-voice at any time should identify the current voice, the voice description information (described below) will relate this name to properties identifying it.
24.3 Defining a new voice

As there are a number of voices available for Festival and they may or may not exists in different installations we have tried to make it as simple as possible to add new voices to the system without having to change any of the basic distribution. In fact if the voices use the following standard method for describing themselves it is merely a matter of unpacking them in order for them to be used by the system.

The variable voice-path conatins a list of directories where voices will be automatically searched for. If this is not set it is set automatically by appending `/voices/' to all paths in festival load-path. You may add new directories explicitly to this variable in your `sitevars.scm' file or your own `.festivalrc' as you wish.

Each voice directory is assumed to be of the form

LANGUAGE/VOICENAME/

Within the VOICENAME/ directory itself it is assumed there is a file `festvox/VOICENAME.scm' which when loaded will define the voice itself. The actual voice function should be called voice_VOICENAME.

For example the voices distributed with the standard Festival distribution all unpack in `festival/lib/voices'. The Amercan voice `ked_diphone' unpacks into

festival/lib/voices/english/ked_diphone/

Its actual definition file is in

festival/lib/voices/english/ked_diphone/festvox/ked_diphone.scm

Note the name of the directory and the name of the Scheme definition file must be the same.

Alternative voices using perhaps a different encoding of the database but the same front end may be defined in the same way by using symbolic links in the langauge directoriy to the main directory. For example a PSOLA version of the ked voice may be defined in

festival/lib/voices/english/ked_diphone/festvox/ked_psola.scm

Adding a symbole link in `festival/lib/voices/english/' ro `ked_diphone' called `ked_psola' will allow that voice to be automatically registered when Festival starts up.

Note that this method doesn't actually load the voices it finds, that could be prohibitively time consuming to the start up process. It blindly assumes that there is a file `VOICENAME/festvox/VOICENAME.scm' to load. An autoload definition is given for voice_VOICENAME which when called will load that file and call the real definition if it exists in the file.

This is only a recommended method to make adding new voices easier, it may be ignored if you wish. However we still recommend that even if you use your own convetions for adding new voices you consider the autoload function to define them in, for example, the `siteinit.scm' file or `.festivalrc'. The autoload function takes three arguments: a function name, a file containing the actual definiton and a comment. For example a definition of voice can be done explicitly by

(autooad voice_f2b  "/home/awb/data/f2b/ducs/f2b_ducs" 
     "American English female f2b")))

Of course you can also load the definition file explicitly if you wish.

In order to allow the system to start making intellegent use of voices we recommend that all voice definitions include a call to the function voice_proclaim this allows the system to know some properties about the voice such as language, gender and dialect. The proclaim_voice function taks two arguments a name (e.g. rab_diphone and an assoc list of features and names. Currently we require language, gender, dialect and description. The last being a textual description of the voice itself. An example proclaimation is

(proclaim_voice
 'rab_diphone
 '((language english)
   (gender male)
   (dialect british)
   (description
    "This voice provides a British RP English male voice using a
     residual excited LPC diphone synthesis method.  It uses a 
     modified Oxford Advanced Learners' Dictionary for pronunciations.
     Prosodic phrasing is provided by a statistically trained model
     using part of speech and local distribution of breaks.  Intonation
     is provided by a CART tree predicting ToBI accents and an F0 
     contour generated from a model trained from natural speech.  The
     duration model is also trained from data using a CART tree.")))

There are functions to access a description. voice.description will return the description for a given voice and will load that voice if it is not already loaded. voice.describe will describe the given given voice by synthesizing the textual description using the current voice. It would be nice to use the voice itself to give a self introduction but unfortunately that introduces of problem of decide which language the description should be in, we are not all as fluent in welsh as we'd like to be.

The function voice.list will list the potential voices in the system. These are the names of voices which have been found in the voice-path. As they have not actaully been loaded they can't actually be confirmed as usable voices. One solution to this would be to load all voices at start up time which would allow confirmation they exist and to get their full description through proclaim_voice. But start up is already too slow in festival so we have to accept this stat for the time being. Splitting the description of the voice from the actual definition is a possible solution to this problem but we have not yet looked in to this. 
