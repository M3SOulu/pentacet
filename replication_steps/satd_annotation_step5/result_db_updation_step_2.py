import json
import psycopg2


def update_satd_affliction_features():
    update_sql = """update comment_attr set satd_affliction = %s where comment_id = %s"""
    update_satd_feature_sql = """update comment_attr set satd_feature = %s where comment_id = %s"""
    db_conn = None
    db_cur = None
    return_msg = 'success'
    impacted_rows = None
    try:
        db_conn = psycopg2.connect(database="pentacet", user='postgres', password='postgres', host='127.0.0.1',
                                   port='5432')
        db_cur = db_conn.cursor()
        satd_affliction_dict = load_json_data(affliction_inp_json_file)
        satd_feature_dict = load_json_data(feature_inp_json_file)
        cmnt_cntr=0
        for comment_id in satd_affliction_dict:
            if satd_affliction_dict[comment_id] == "SATD":
                cmnt_cntr += 1
                #print("Processing {} comment out of {} comments".format(cmnt_cntr, len(satd_affliction_dict.keys())))
                db_cur.execute(update_sql, (satd_affliction_dict[comment_id], comment_id))
                db_cur.execute(update_satd_feature_sql, (satd_feature_dict[comment_id], comment_id))
                print("updating {}/{} resulted in {}".format(cmnt_cntr, len(satd_affliction_dict), db_cur.rowcount))

        return_msg = "updated successfully"  #+ str(impacted_rows) + " rows successfully."
        db_conn.commit()
        db_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return_msg = error
        db_cur.close()
    return return_msg


def load_json_data(json_file):
    return json.loads(open(json_file,"r",encoding='utf-8').read())


##################################################
affliction_inp_json_file='C:\\Users\\msridhar20\\parallelize_satd_annotation\\c4\\c4_satd_affliction_v2_2.json'
feature_inp_json_file='C:\\Users\\msridhar20\\parallelize_satd_annotation\\c4\\c4_satd_features_v2_2.json'

update_satd_affliction_features()



