from google.appengine.ext import db
from entities import *
from datetime import datetime
from google.appengine.api import users, memcache


"""
Adds a new entry for the current user.
"""
def new_entry(link, tags, date_expires=None):
    owner = get_owner()
    def store_new_entry():
        #create and store the entry
        entry = Entry(parent=owner,
                      link=link, 
                      date_expires = date_expires,)
        entry_key = entry.put()    
        
        #ensure an entity exists for each tag
        existing_tags = Tag.get_by_key_name(tags, parent=owner)
        def upsert_tag((tag, tag_entity)):
            if tag_entity is None:
                tag_entity = Tag(parent=owner, key_name=tag)
            tag_entity.last_used = datetime.now()
            tag_entity.entries_tagged.append(entry_key)
            tag_entity.times_used += 1
            return tag_entity
            
        to_set = map(upsert_tag, zip(tags, existing_tags))
        
        #save tags
        db.put(to_set)
    
    #db.run_in_transaction_options(db.create_transaction_options(xg=True), store_new_entry)
    store_new_entry()
    
    
"""
Fetches all tags for the current user.
"""
def get_all_tags():  
    owner = get_owner()
    
    def fetch_tags():
        q = Tag.all()
        q.ancestor(owner)
        q.order("-times_used")
        q.order("-last_used")
        return q.fetch(100)
    
    return fetch_tags() 
    #return cache_entity(__cache_key("all_tags"), fetch_tags)


"""
Fetches the current user's Owner entity
"""
def get_owner():
    user = users.get_current_user()
    
    def fetch_owner():
        q = Owner.all()
        q.filter("user =", user)
        owner = q.get()
        #create if does not exist yet
        if owner is None:
            owner = Owner()
            owner.put()   
        return owner
    
    return cache_entity(__cache_key("Owner"), fetch_owner)


"""
Fetches a short list of all recent entries
"""
def get_recent_entries():
    #get the most recent entries
    q = Entry.all()
    q.ancestor(get_owner())
    q.order("-date_created")
    return q.fetch(10)


"""
Fetches a list of entries that match the specified tags
"""
def search_by_tags(tags):
    entry_ids = None
    #get a set of entry id's that represent entries that match all tags specified
    tag_entities = Tag.get([db.Key.from_path("Owner", get_owner.key().id(), "Tag", t) for t in tags])
    #filter out any null tags (these arrise when people provide non-existent tags)
    tag_entities = [te for te in tag_entities if te is not None]
    for t in tag_entities:
        if entry_ids is None:
            entry_ids = set(t.entries_tagged)
        else:
            entry_ids = entry_ids & set(t.entries_tagged)
    #fetch the specified entries
    return Entry.get(entry_ids)
        
        
def cache_entity(cache_key, fetch_func):
    entity = memcache.get(cache_key)
    if entity is None:
        entity = fetch_func()
        memcache.add(cache_key, entity, 60)    
    return entity 

def __cache_key(type_id):
    user = users.get_current_user()
    return "%s_%s" % (type_id, user.email())