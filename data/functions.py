from google.appengine.ext import db
from entities import *
from datetime import datetime
from google.appengine.api import users


"""
Adds a new entry for the current user.
"""
def new_entry(link, tags, date_expires=None):
    user = get_user()
    def store_new_entry():
        #create and store the entry
        entry = Entry(parent=user,
                      link=link, 
                      date_expires = date_expires,)
        entry_key = entry.put()    
        
        #ensure an entity exists for each tag
        existing_tags = Tag.get_by_key_name(tags, parent=user)
        def upsert_tag((tag, tag_entity)):
            if tag_entity is None:
                tag_entity = Tag(parent=user, key_name=tag)
            tag_entity.last_used = datetime.now()
            tag_entity.entries_tagged.append(entry_key)
            return tag_entity
            
        to_set = map(upsert_tag, zip(tags, existing_tags))
        
        #save tags
        db.put(to_set)
    
    #db.run_in_transaction_options(db.create_transaction_options(xg=True), store_new_entry)
    store_new_entry()
    
    
"""
Fetches all tags for the current user.
"""
def get_all_tags(tag_names_only=True):  
    q = Tag.all(keys_only=tag_names_only)
    q.ancestor(get_user())
    tags = q.fetch(100)
    if tag_names_only:
        return [t.name() for t in tags]    
    else:
        return tags


"""
Fetches the current user's User entity
"""
def get_user():
    q = User.all()
    q.filter("user =", users.get_current_user())
    user = q.get()
    #create if does not exist yet
    if user is None:
        user = User()
        user.put()
    return user


"""
Fetches a short list of all recent entries plus the tags for each entry
"""
def get_recent_entries():
    #get the most recent entries
    q = Entry.all()
    q.order("-date_created")
    entries = q.fetch(10)
    
    #get the tags that reference the recent entries
    q = Tag.all()
    q.filter("entries_tagged IN", entries)
    tags = q.fetch(100)
    
    #map them together
    return map(lambda e: (e, filter(lambda t: e.key() in t.entries_tagged, tags)), entries)

