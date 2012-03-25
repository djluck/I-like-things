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
Fetches a short list of all recent entries
"""
def get_recent_entries():
    #get the most recent entries
    q = Entry.all()
    q.order("-date_created")
    return q.fetch(10)


"""
Fetches a list of entries that match the specified tags
"""
def search_by_tags(tags):
    entry_ids = None
    #get a set of entry id's that represent entries that match all tags specified
    tag_entities = Tag.get([db.Key.from_path("User", get_user().key().id(), "Tag", t) for t in tags])
    #filter out any null tags (these arrise when people provide non-existent tags)
    tag_entities = [te for te in tag_entities if te is not None]
    for t in tag_entities:
        if entry_ids is None:
            entry_ids = set(t.entries_tagged)
        else:
            entry_ids = entry_ids & set(t.entries_tagged)
    #fetch the specified entries
    return Entry.get(entry_ids)
        