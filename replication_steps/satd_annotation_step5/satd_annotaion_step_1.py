import re
import traceback
import pandas as pd
import numpy as np
import json
from multiprocessing import cpu_count, Pool



 
satd_features = ['hack ', ' retarded', ' ugly', 'problematic', ' hacky',
                     ' silly', ' workaround', ' work-around', 'temporary solution', ' crutch',
                     ' messed', 'bullshit', ' abandoning', ' toss', ' barf', 'yuck', 'unhappy', 'kludge',
                     ' uncool', ' kaboom', ' xxx:', 'fixme', 'todo', 'to-do', 'fix me', 'xx[x]+:',
                     'deficiency', 'hurts', 'soft error', 'not right', 'trial and error',
                     'hang our heads in shame', 'not solid', 'isnt solid', "isn't solid",
                     'something bad', 'doesnt look right', "doesn't look right", " spoof ", " kiddie", " dumb ",
                     " retard",
                     " moronic", " retarted", " pathetic", " ridiculous", " ignorant", " moron", " asinine",
                     " clueless", " naive", "more trouble",
                     " delusional", " childish", " petty", " fucking idiot", " lame", " bull shit", " unintelligent",
                     " hypocritical", " douchy",
                     " idiot", " potential loss", " major loss", " other loss", " more loss", " possible loss",
                     " recent loss", " terrible loss",
                     " devastating loss", "huge loss", "terrible loss", "unexpected loss", "such loss", "massive loss",
                     " hideous", " fugly",
                     " uglier", " careless", "rats ass", " upset", " bother", "literally nothing",
                     "just an idiot", " untrue", "total bullshit", " misinterpreting", " nonsense", " misinformed",
                     " insinuating",
                     " undesirable", " trouble", " contentious", " troubling", "big issue", " damaging", "major issue",
                     " prevalent", "bigger issue",
                     " major problem", " nebulous", " detrimental", " unproblematic", "bigger problem",
                     "counter productive", " counterproductive",
                     " counter-productive", " dubious", "real issue", "bigger issue", "different issue",
                     "significant problem",
                     " main issue", "real problem", " uncontroversial", " undetermined", " undiscovered",
                     " speculated", " pointless", " absurd", " comical", " preposterous", " ironic", "looks bad",
                     " outlandish", " bizarre", " nitpick", " ludicrous", "temporary fix", "work around", "simple fix",
                     " real fix", "known bug", "possible fix", " pity", " awful", "missed opportunity", " shameful",
                     " embarassment", " travesty", " disappointment", " bummer", " excuse", "such crap", "sad thing",
                     " horrible",
                     " sad ", "sickening", "wasted opportunity", "sadly", "temporary solution", "temp sol", "temp fix",
                     "temporary fix",
                     " best solution", "viable solution", "more permanent solution", "best fix", "better solution",
                     "short term solution",
                     " only solution", "quick fix", "ideal solution", "other solution", "only solution", "perfect fix",
                     "temporary measure",
                     " easiest solution", "bad solution", "easy solution", "simple solution", "easy fix",
                     " proper solution", "obvious solution",
                     " real solution", "easy solution", "easier solution", "easier fix", " exacerbate",
                     " worsen", "main cause", " alleviates", " aggravates", "actual cause", " exacerbating", " lessen",
                     " primary cause", "specific issue", "minor issue", "current issue", "small issue", "many issues",
                     "obvious problem",
                     " signficant issue", "potential problem", "potential issue", " just an issue", " shitty",
                     " aweful", " horrid ", " worse ",
                     " sucks", " crappy", " lousy", " horrendous", " crazy", " fucked", "bad lol", " messy",
                     " bull crap", "non sense", " non-sense", " nonsense", " horseshit", " hogwash", " malarkey",
                     " major risk", "significant risk", "possible risk", "bigger risk", "only risk", "huge risk",
                     "large risk", "great risk",
                     " inherent risk", "higher risk", " wreck", " bust", " sabotaging", " sabotage", " forsaking",
                     " dooming",
                     " despising", " resent", " undermining", " appeasing", " shunning", " shun", " patching",
                     " rectify", " remedy",
                     " unfixable", " bandaid", " band aid", " band-aid", " dogshit", 'sh!t', 's\\*\\*t', 'sh\\*t',
                     " goddamn", " damn", " heck",
                     " ewww", " ugh", " blegh", " glitch", " glitchy", " bugginess", " unoptimized", " bugfest",
                     " dissatisfied",
                     " miserable", " upset", " upsetting", " regretful", " hopeless", " selfish", " disgruntled",
                     " uncool", " douchey", " juvenile", " obnoxious", " immature", " embarrasing", " assholish",
                     " silly", " crass",
                     " cringey", " cringy", " disrespectful", " dorky", " sloppiness", "major flaw",
                     " glaring problem", " flaw ", " ditch", " inefficiency", " wasteful", " inefficiently",
                     "impractical",
                     " unfeasible", " uneconomical", " laborious", " unsustainable", " deficiency", " deficient",
                     " deficiencies", " irritate", "dont care", "don't care", "does not care", "who care",
                     "do not care",
                     " dont think", "don't think", "not good", "too expensive", "its expensive", "it's expensive",
                     " for now", "slow route", "too slow", "performance overhead", "not optimal", "need to figure",
                     " no idea", "foul", " will not work", " wont work", " won't work", " not working", " does it work",
                     " does it", " work only", " work correctly only if", " only works", " works only if",
                     " additional test required",
                     " additional work required", " cant afford", " can't afford", " shouldnt be necessary",
                     " shouldn't be necessary",
                     " isnt a great", " isn't a great ", " isnt great ", " isn't great ", " is not great ",
                     " unexpected eof", " shouldnt happen", " shouldn't happen", " should never happen",
                     "should not happen",
                     "confusing", "sneaky", "evade", "can[']*t tolerate", "can[']*t tolerate", "can[\s]*not tolerate",
                     "could not tolerate",
                     "bad design", "actually bad", "too bad", "bad for performance", "bad for various" "bad code",
                     "this is bad", "definitely bad",
                     "is this bad", "badness", "least risky", "but if it doesn't", "no other [(known)\s]*way",
                     "catch[-|\s]*22",
                     "to work properly", "for some reason", "stops complaining", "burn[(ing)]* the cpu",
                     "burn[(ing)]* the code",
                     "burning cpu", "burning code",
                     "time consuming", "directly impact", "this is dangerous", "don[']*t even start",
                     "unclear how to handle",
                     "consuming cpu", "recurse indefinitely", "doesn[']*t make sense", "does not make sense",
                     "doesn't make a whole lot of sense", "are slower", "is slower", "not [(the)*\s]?patch[(ed)]*",
                     "not [(a)*\s]*good [(thing)]*",
                     "but [(it)?\s]*works", "for it to work", "oddly", "must not be used in version", "odd choice",
                     "odd way", "fix blatant", "fudged", "to fix", "fix compatibility",
                     "fix later", "temporary [(test)?\s]*code", "can[']*t deal", "can[\s]*not deal", "could not deal",
                     "idk ","idk,","idk\\.", "very mad", "still[\s]*a[\s]*problem", "does not work", "doesn[']*t work",
                     "not [a\s]*secure",
                     "not [\w\s]*good", "temp[(orary)]* fix", "don[']*t think this [(will)?\s]*work[s]*",
                     "this is wrong",
                     "is hell[,|\\.]* ", "the hell[,|\\.]* ", "hell yeah", "can[']*t hurt", "don[']*t know",
                     "do not know", "shouldn[']*t be necessary",
                     "no idea", "we [(now)?\s]*have to deal", "need to deal", "doesn[']*t [(seem to)?\s]*help",
                     "can[']*t [(do much)|(be)]+ useful", "[(silently)?\s]*ignore inconsistencies",
                     "not perfect", "no longer recommended", "try to optimize", "don[']*t support",
                     "test doesn[']*t pass", "should change this", "needs* change","needs* optimization",
                     "needs* to be changed", "needs* to be modified", "needs* to be optimized",
                     "what if", "this is incorrect", "decompiled incorrectly", "more gracefully", "inconsistent code",
                     "something is wrong", "may[\s]*be this is", "whacky", "will probably fail",
                     "don[']*t validate too much",
                     "dirty fix", "bit dirty", "very dirty", "dirty trick", "dirty work", "dirty solution", "dirty but",
                     "but works", "dirty [(little)\s]*shortcut", "too lazy", "lazy and", "lazy since", "lazy creation",
                     "intentionally lazy", "lazy processing", "lazy as", "strange issue", "performance issue",
                     "security issue",
                     "known issue", "weird issue", "still an issue", "talkback issue", "don[']*t do this", "bail here",
                     "best effort", "best attempt", "move it temporarily", "can be revisited", "not best", "not ideal",
                     "not the best", "not the ideal", "a nasty", "the nasty", "but not necessary",
                     "may\s*be not necessary",
                     "atleast it works", "got to make this", " damn", "fairly nasty", "nasty heuristic",
                     "is not necessary",
                     "lighten it", "not sure", "a mess ", "will mess ", "[m]*ucky", "this is vulnerable",
                     "makes [\w\s*]*vulnerable",
                     "avoid creation of", "make[s]* sense if", "optional optimization",
                     "not necessary yet", "get rid", "shame on", "strangely", "very strange", "little annoying",
                     "strange bug",
                     "tmp fix", "temp fix", "tmp patch", "temp patch", "temporary patch", "strange mystery",
                     "strange behavio[u]*r", "strange happens",
                     "sound strange", "strange effect", "not thorough enough", "strange enough",
                     "strange things happen",
                     "strange implementation", "really strange", "terrible consequences", "something terrible",
                     "cause terrible",
                     "terrible idea", "terrible implementation", "terrible[\\.]+", "some issues [(with)\s]*implement",
                     "bit tricky", "very tricky", "tricky code", "bad code", "little trick", "extra tricky",
                     "really tricky", "troublesome",
                     "dirty trick", "tricky problem", "tricky code", "strange trick", "is tricky", "get tricky",
                     "small trick",
                     "this trick", "weird generic", "do not use in",
                     "is a trick", "nasty trick", "trick to", "in trouble", "s unfortunate", "unfortunately", "afaik",
                     "kind of uncertain", "is uncertain", "is unnecessary", "should be unnecessary", "^unnecessary$",
                     "unnecessary[\\.]*$", "probably unnecessary", "an unnecessary", "unnecessary code",
                     "avoid unnecessary",
                     "weird situation", "weird code", "weird block", "is weird", "weird property", "weird error",
                     "weird case",
                     "weird bug", "weird[\\.]+", "weird way", "bit weird", "weirdly", "really weird",
                     "weird observation",
                     "weird thing", "get weird", "little weird", "weird bug", "weird but", "^weird$", "to stop weird",
                     "weird error", "didn[']?t make sense", "don[']?t make sense", "seems [(to be)\s]*useless",
                     "^useless$", "useless for this", "this is useless", "pretty useless", "bad for performance",
                     "are useless", "apparently useless", "now useless", "useless if", "useless here",
                     "completely useless",
                     "probably useless", "e[s]*entially useless", "now useless", "useless impl", "weak code",
                     "pretty weak",
                     "but why", "might have issues", "this should not happen", "this shouldn[']?t happen",
                     "worry right now",
                     "^shouldn[']*t worry", "worry about this", "significantly worse", "make it scale", "worse than",
                     "even worse", "major security implications", "eliminate [\w\s*]*complexity", "worse alternatives",
                     "will probably fail", "^bail\s*out$", "something seriously wrong", "it would be nice",
                     "something is\s*n['|o]*t right",
                     "ignore potential failures*", " prune ", " pruning " "tests are failing", "suspect that",
                     "is\s*n['|o]*t bulletproof", "for later",
                     " deliberately", "went horribly wrong", "likely [(to be)\s]*wrong", "because of bug",
                     "gone terribly wrong", "gone horribly wrong", "is terribly wrong", "is horribly wrong",
                     "went terribly wrong",
                     "bug gives", "no reason", "wrong implementation", "can['|(no)]*t happen", "sometimes is wrong",
                     "really wrong",
                     "probably wrong", "should we", "do we", "could go wrong", "wrong[\\.]", "wrong$", "this is wrong",
                     "should\s*n['|o]*t get here",
                     "vague behavior", "buggy[\\.|\\?]*$", "somewhat buggy", "buggy part", "^buggy", "^don[']*t care$",
                     "don[']*t care[\\.|!]*$",
                     "don[']*t care if this fails", "is an inconsistency", "correct an inconsistency",
                     "slight inconsistency",
                     "is some inconsistency", "not the perfect place", "undocumented so far", 
                     "are more expensive", "a short[-|\s]*cut",
                     "much more expensive", "is more expensive", "this is dangerous", "not as efficient ",
                     "this is far from", "short[-|\s]*cut for",
                     "^no need to", "need to remove", "can be simplified", "do not use", "^short[-|\s]*cut",
                     "in the future [(is)|(it)]+",
                     "removed in the future", "change in the future", "possibl[e|y]+ [a\s]*bug", "can take time",
                     "room for optimization",
                     "can be more efficient", "cheap hack", "do not use this", "do not use unless you are sure",
                     "do not use [\w*[\\.]*\w*]*[()]*\s*[(here)|(in)|(on)]*",
                     "do not use[\\.]?$", "added here as convenience", "does not work", "may be later",
                     "avoid an implementation",
                     "we have side\s*effect", "last resort", "we don[']*t know", "pity",
                     "has [(the)?\s*]*side[-|\s]*effect", "is stupid",
                     "seemingly stupid", "kind['|\s]*[a|(of)]*\s*stupid", "quite stupid", "stupidly inefficient",
                     "stupid hack",
                     "must have been removed", "clumsy", "have to temporarily", "temporarily and ", "had [\w\s*]*bugs",
                     "^temporarily",
                     "should never occur", "cheat here", "mem[(ory)]* waste", "waste of",
                     "doesn[']*t work properly", "doesn[']*t work well", "doesn[']*t work hence",
                     "doesn[']*t work perfectly",
                     "that doesn[']*t work", "code doesn[']*t work", "doesn[']*t seem to help",
                     "this should be considered",
                     "this should be changed", "this should be [a|in]+ separate", "this should be impossible",
                     "but have this code",
                     "should be reasonably", "should be discarded", "eventually this should be",
                     "may\s*be this should be",
                     "really this should be", "in any case this should be", "^in future", "considered unsafe",
                     "^unsafe",
                     "this should be o*k", "don[']*t do this", "unsafe at present", "so we need to", "not very fast",
                     "is that ok",
                     "is that fine", "would be redundant", "would be much easier", "would be more precise",
                     "would be more compact",
                     "code is unsafe", "code is inherently unsafe", "code is crazy", "to work properly",
                     "for work properly",
                     "should be no[-]*op ", "wish [i\s]*could", "this part sucks", "^revisit", "don[']*t know",
                     "technically incorrect",
                     "incorrect here", "hangs on some", "useless check", "useless validation", "skip optimization",
                     "note to the future",
                     "hope there will be no", "work in progress", "eventually this should be", "maybe this should be",
                     "special cheat[s]*",
                     "special cheat[s]* that speed", "never a valid solution", "this method incorrectly",
                     "implementation is temporary",
                     "is inefficient", "made clearer", "not necessary to call", "not necessary to invoke",
                     "not necessary to declare",
                     "not be hard to eliminate", "should be broken down", "this is stupid", "better way to handle",
                     "can[']*t do this in",
                     "somewhat of a hack", "should clean this", "need some synchronization", "could factor it",
                     "this is broken",
                     "only way to fix", "need[s]* to be done", "doesn[']*t seem\s*[very]*correct", "silly bug",
                     "sloppy hack",
                     "weird hack", "this sucks", "hack to avoid", "temporary hack", "hack to", "crap like this",
                     "nasty hardcoded",
                     "do this hack until", "better way of fixing", "bad way of doing", "this is nasty",
                     "shouldn[']*t be public",
                     "hack since", "is messy", "should be rewritten", "hence this hack", "temporary impl", "bad hack",
                     "need to add",
                     "probably break", "is wrongly called", "to make sense", "has insufficient information", "mac hack",
                     "windows hack",
                     "hack in order", "just temporary for", "temporary and will go away", "just temporary",
                     "should probably be",
                     "hate this so much", "not sure why", "is there no better way", "is there no better way",
                     "need a better mechanism",
                     "yet to be agreed", "works but", "really ought to have", "work required on", "really a problem",
                     "need replacing",
                     "no longer has this", "would be sensible", "not implemented yet", "work any better",
                     "programming error",
                     "needs more work", "we have a problem", "won[']*t work", "may\s*be replaced later", "slight hack",
                     "more efficient", "hack:", "optimization:", "we know this fails", "only work if", "works only on",
                     "don[']*t appear to work", "this is problematic", "like[l]*y a bug", "know how to deal",
                     "flickering like hell",
                     "do[']*nt work under", "not a good way", "doesn[']*t meet new requirements", "total hack",
                     "causes problems",
                     "best way to get around the problem", "bit slack", "required otherwise", "silently ignore",
                     "hard\s*coded but",
                     "a bit questionable", "a hack", "logically not sufficient", "i hope", "work-around",
                     "unfortunately we need to",
                     "perhaps more elegantly", "not sure if this is", "we really should", "not yet ready", "future:",
                     "need better test",
                     "does not work", "real[ly]* stupid", "cleanup:", "is wrong here", "hackish", "we don[']*t want",
                     "problem:",
                     "currently only here", "we basically ignore protocol", "silly optimization", "it would be nice",
                     "need to reexamine",
                     "bit risky if", "this is gross", "inefficient timewise", "not a compelling reason",
                     "this is still ugly",
                     "specific hack for", "not sure how well", "not sure", "not efficient", "don[']*t bother to check",
                     "lame issue", "to meet deadline",
                     "is lame", "it[']*s lame", "lame generics issue", "ideally this hack should be",
                     "rather ugly hack",
                     "still not implemented", "unused but", "would be nice to", "here[']*s a quirk",
                     "probably be a little faster",
                     "need[s]* to be improved", "know it[']*[s\s*]*bad", "better idea", "could make this",
                     "won[']*t compile with",
                     "this should never be called", "revisit:", "kind of hacky", "it is not [very\s]*clear",
                     "hate to admit","considering time(-)*\s*constraint[s]*","to time(-)*\s*constraint[s]*",
                     "appears to be bug", "far from being perfect", "but should work", "not sure what",
                     "really irritating", "for want of time", 
                     "is a remnant of prev", "otherwise we will get", "have to think about", "not sure whether",
                     "will be processed later", "work on this later",
                     "re(-)*engineer ", "refactor it", "refactor this", "refactor the",
                     "refactor to have", "broken class", "broken method", "broken interface", "broken enum",
                     "broken file", "broken package", "live with this", "live with it", "live with that",
                     "looks bad", "broken static block", "is not correct", "fuck things up", "wonder if",
                     "wish i could", "issues to resolve", "redundant with", "could refactor",
                     "is a nightmare", "re(-)*evaluate this", "could be smarter", "could be static", "particularly nasty",
                     "stupid:",
                     "this part sucks", "piss me off", "stupidity", "^stupid", "we would want to", "makes no sense",
                     "feels sloppy", "it[']*s weird", "slows down",
                     "fuck me dead", "^not needed$", "empty implementation", "is never called", "not sure why",
                     "effectively same as", "^not\s*used", "^lazy$", "never happens", "can never happen",
                     "may\s*be do nothing", "change this when ",
                     "this is [a\s*]*weird", "make it more elegant", "more slower",
                     "should we ", "should this ", "should the ", "do we [(need)|(have)]+ to", "does this ", "does it ", 
                     "is not correct", " is incorrect", "poorly designed", "poor design", "poor implementation",
                     "should the ", "when do ", "shouldn[']*t we ", "shouldn[']*t it ", "shouldn[']*t the ", 
                     "how can ", "how does ", "do we ", "do these ", "why are ", "why this ", "shouldn[']*t this ",
                     "why do ","why is ", "why both of ", "is this right",
                     "can this be ", "is this ", "can we ", "can this be?","\\.can this", 
                     "^can this ", " can this", "does anyone ", "how to handle", "is it\\?", "is it ", "what to do ",
                     "but it currently isn[']*t","tbd:", "no reliable way", "best guess", "opt for easy way",
                     "does this lazily","we will try",
                     "earliest version supported", "^not used", "currently not used", "currently unused",
                     "for legacy reasons", "not currently used"]

def satd_feature_match_and_update(x):

    feat = None
    try:
        matching_features = []

        for feat in satd_features:
            if feat.lower() == "idk " or feat.lower() == "idk," or feat.lower() == "idk.":  ## only for feature 'idk' combining multiple regex using and
                if re.search(feat.lower(), x.lower()) and not re.search(
                        "copyright", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() == "to fix":
                if  re.search(feat.lower(), x.lower()) and not re.search("copyright", x.lower()) and not re.search("license", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() == "for later":
                if  re.search(feat.lower(), x.lower()) and not re.search(" see ", x.lower()) and not re.search(" git", x.lower()) and not re.search(" use", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() == "should not happen":
                if  re.search(feat.lower(), x.lower()) and not re.search("exception", x.lower()) and not re.search(" throws", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() ==  "wrong$":
                if  re.search(feat.lower(), x.lower()) and not re.search("exception", x.lower()):
                    matching_features.append(feat)            
            elif feat.lower() ==  " for now":
                if  re.search(feat.lower(), x.lower()) and not re.search("copyright", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() ==  "^no need to":
                if  re.search(feat.lower(), x.lower()) and not re.search(" so", x.lower()):
                    matching_features.append(feat)                   
            elif feat.lower() ==  "we don[']*t want":
                if  re.search(feat.lower(), x.lower()) and not re.search("so we", x.lower()):
                    matching_features.append(feat)                   
            elif feat.lower() == "wrong[\\.]":
                if  re.search(feat.lower(), x.lower()) and not re.search("if anything", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() == " deliberately" or feat.lower() == " does it" or feat.lower() == "does it ":
                if  re.search(feat.lower(), x.lower()) and not re.search("copyright", x.lower()) and not re.search("license", x.lower()) and not re.search("warrant", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() == "is this ":
                if  re.search(feat.lower(), x.lower()) and re.search("\\?", x.lower()):
                    matching_features.append(feat)
            elif feat.lower() == "is it ":
                if  re.search(feat.lower(), x.lower()) and re.search("\\?", x.lower()):
                    matching_features.append(feat)
            else:
                if re.search(feat.lower(), x.lower()):
                    matching_features.append(feat)
        return ','.join(matching_features)
    except Exception as reg_exception:
        error_message = traceback.format_exc()
        print("Unexpected exception while processing SATD ANNOTATION: {}, {}".format(x, feat))
        print("Error details: {}".format(error_message))
        return "error"


def process_comment(df):
    df['satd_features'] = df['cleaned_comment'].apply(satd_feature_match_and_update)
    df['satd_affliction'] = df['satd_features'].apply(lambda x: 'SATD' if len(x) > 0 else 'NON_SATD')
    return df


def parallelize_dataframe(df, func, n_cores=16):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def save_json(json_dict, file_name):
    json_object = json.dumps(json_dict, indent=4, ensure_ascii=False)
    with open(file_name, "w", encoding="utf8") as outfile:
        outfile.write(json_object)


##############################################################################
if __name__ == '__main__':
    
    inp_cmnt_df = pd.read_csv('/scratch/project_2002565/parallelize_satd_annotation/c1/c1_cleaned_nl_comments_v2.tsv', sep='\t', encoding='utf8',names=['comment_id','cleaned_comment'])
    inp_cmnt_df['is_null'] = inp_cmnt_df['cleaned_comment'].isnull()

    print("Total rows that are classified as NL",len(inp_cmnt_df))
    cmnt_df = inp_cmnt_df.loc[inp_cmnt_df['is_null'] != True]
    print("Total rows that are non null: ",len(cmnt_df))
    print("Total empty or null rows: ",len(inp_cmnt_df) - len(cmnt_df))
    cmnt_column = 'cleaned_comment'

    print("Total features: {}".format(len(satd_features)))
    sf = 0
    mf = 0
    for feat in satd_features:
        if len(feat.strip().split(' ')) > 1:
            sf+=1
        else:
            mf+=1
    print("Total single word feature count:",mf)
    print("Total multi word feature count:",sf)


    updated_cmnt_df = parallelize_dataframe(cmnt_df, process_comment)
    processed_satd_affliction_dict = dict(zip(updated_cmnt_df.comment_id, updated_cmnt_df.satd_affliction))
    processed_satd_features_dict = dict(zip(updated_cmnt_df.comment_id, updated_cmnt_df.satd_features))
    save_json(processed_satd_affliction_dict, "c1_satd_affliction_v2_2.json")
    save_json(processed_satd_features_dict, "c1_satd_features_v2_2.json")



