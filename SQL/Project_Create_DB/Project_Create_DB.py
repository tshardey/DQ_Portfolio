
# coding: utf-8

# # Building a Database
# 
# - Import data into SQLite
# - Design a normalized database schema
# - Create tables for our schema
# - Insert data into our schema
# 
# We will be working with a file of Major League Baseball games from Retrosheet. Retrosheet compiles detailed statistics on baseball games from the 1800s through to today. 

# In[3]:


# Setting up the environment
import pandas as pd
import sqlite3

pd.set_option('max_columns', 180)
pd.set_option('max_rows', 200000)
pd.set_option('max_colwidth', 5000)


# ## Importing Data

# In[4]:


# Reading in the data into dataframes

game_log = pd.read_csv("game_log.csv")
park_codes = pd.read_csv("park_codes.csv")
person_codes = pd.read_csv("person_codes.csv")
team_codes = pd.read_csv("team_codes.csv")


# In[5]:


# Previewing data
print("The shape of the dataframe is: " + str(game_log.shape))
print("\nGame Data:")
game_log.head(3)


# In[6]:


print("The shape of the dataframe is: " + str(park_codes.shape))
print("\nPark Data:")
park_codes.head(3)


# In[7]:


print("The shape of the dataframe is: " + str(person_codes.shape))
print("\n Person Data:")
person_codes.head(3)


# In[8]:


print("The shape of the dataframe is: " + str(team_codes.shape))
print("\n Team Data:")
team_codes.head(3)


# ## Data Preview Observations:
# 
# Game Data Associations:
# - park_id in park_codes corresponds to park_id in game_log
# - id in person_codes corresponds to a number of position specific columns in game_log
# - team_id in team_codes corresponds to v_name and h_name (visitor and home team) in game_log

# ## Dataframes to SQL

# In[9]:


# Creating a function to quickly run queries
def run_query(q):
    with sqlite3.connect('mlb.db') as conn:
        return pd.read_sql(q, conn)
    
# A function to run SQL commands
def run_command(c):
    with sqlite3.connect('mlb.db') as conn:
        conn.isolation_level = None
        conn.execute(c)


# In[10]:


# setting up the connection
conn = sqlite3.connect("mlb.db")


# In[11]:


# Propagating mlb database 
game_log.to_sql("game_log", conn, index=False)
park_codes.to_sql("park_codes", conn, index=False)
person_codes.to_sql("person_codes", conn, index=False)
team_codes.to_sql("team_codes", conn, index=False)


# In[12]:


# Creating an index for the game_log table
c_game_id = "ALTER TABLE game_log ADD game_id"
c_set_game_id = '''
UPDATE game_log 
SET game_id = h_name || date || number_of_game'''

run_command(c_game_id)
run_command(c_set_game_id)

# Checking the addition of the game_id
q_check_game_id = '''
SELECT h_name, 
    date, 
    number_of_game, 
    game_id
FROM game_log
LIMIT 5'''

run_query(q_check_game_id)


# ## Normalization 
# 
# Removing repitition in columns
# - Three columns that relate to one player, followed by three columns that relate to another player 
# - Columns in game_log that have the player ID followed by the player name for each position on the team
#     - This also applies to other personel positions such as umpire or team manager
#     
# Primary key attributes
# - Player names are not attributes of the game_id but of the payer_id
# 
# Redundant data
# - Park information is available in multiple tables
# - League is an attribute of the team_id it appears in park_codes and game_log
# 

# ## Schema
# 
# [schema]: https://s3.amazonaws.com/dq-content/193/mlb_schema.svg "MLB Database Schema"
# 
# The database [schema] optimization: 
# 
# person
# - Each of the 'debut' columns have been omitted, as the data will be able to be found from other tables.
# - Since the game log file has no data on coaches, we made the decision to not include this data.
# 
# park
# - The start, end, and league columns contain data that is found in the main game log and can be removed.
# 
# league
# - Because some of the older leagues are not well known, we will create a table to store league names.
# 
# appearance_type
# - Our appearance table will include data on players with positions, umpires, managers, and awards (like winning pitcher). This table will store information on what different types of appearances are available.

# ## Table Normalization

# In[13]:


# Creating a normalized person table
c_create_person = '''
CREATE TABLE person (
person_id TEXT PRIMARY KEY,
first_name TEXT,
last_name TEXT)'''
    
run_command(c_create_person)


# In[14]:


# Populating the normalized person table
c_pop_person = '''
INSERT INTO person
SELECT 
    id,
    first,
    last
FROM person_codes'''

run_command(c_pop_person)


# In[15]:


# Verifying 
q_person_check = "SELECT * FROM person LIMIT 5"
run_query(q_person_check)


# In[16]:


# Creating a normalized park table
c_create_park = '''
CREATE TABLE park (
park_id TEXT PRIMARY KEY,
name TEXT,
nickname TEXT,
city TEXT,
state TEXT,
notes TEXT);'''
    
run_command(c_create_park)


# In[17]:


# Populating the normalized park table
c_pop_park = '''
INSERT INTO park
SELECT 
    park_id,
    name,
    aka,
    city,
    state,
    notes
FROM park_codes'''

run_command(c_pop_park)


# In[18]:


# Verifying 
q_park_check = "SELECT * FROM park LIMIT 5"
run_query(q_park_check)


# In[19]:


# Looking at the different league codes in order to fill the league table 
park_codes['league'].value_counts()


# In[20]:


# Creating a normalized league table
c_create_league = '''
CREATE TABLE league (
league_id TEXT PRIMARY KEY,
name TEXT);'''
    
run_command(c_create_league)


# In[21]:


# Populating the normalized league table
c_pop_league = '''
INSERT INTO league
VALUES
("NL", "National League"),
("AL", "American League"),
("AA", "Double-A"),
("US", "Union Association"),
("FL", "Florida League"),
("PL", "Player's Association");
'''
run_command(c_pop_league)


# In[22]:


# Verifying 
q_league_check = "SELECT * FROM league"
run_query(q_league_check)


# In[23]:


# Importing appearance_type table into pandas df
appearance_type_df = pd.read_csv("appearance_type.csv")

appearance_type_df.head()


# In[24]:


# Transfering table to mlb.db
appearance_type_df.to_sql("appearance_type_init", conn, index = False)


# In[25]:


# Creating empty table for appearance_type with desired structure
c_create_appearance = '''
CREATE TABLE appearance_type (
appearance_type_id TEXT PRIMARY KEY,
name TEXT,
category TEXT);'''
    
run_command(c_create_appearance)


# In[26]:


# Populating the normalized appearance_type table 
c_pop_appearance = '''
INSERT INTO appearance_type
SELECT *
FROM appearance_type_init'''

run_command(c_pop_appearance)


# In[27]:


# Verifying 
q_appearance_check = "SELECT * FROM appearance_type LIMIT 5"
run_query(q_appearance_check)


# In[28]:


# Creating a normalized team table
c_create_team = '''
CREATE TABLE team (
team_id TEXT PRIMARY KEY,
league_id TEXT,
city TEXT, 
nickname TEXT,
franch_id TEXT,
FOREIGN KEY (league_id) REFERENCES league(league_id));'''
    
run_command(c_create_team)


# In[29]:


# An error occured when trying to get he values from team_codes
team_codes['team_id'].value_counts()


# In[30]:


# There is two instances of the Brewers since they changed leagues in 1998
q_duplicate = "SELECT * FROM team_codes WHERE team_id = 'MIL'"
run_query(q_duplicate)


# In[31]:


# Due to the teams table not perserving the league information the instance of
# the Brewers in the AL league will be dropped

c_delete_duplicate = "DELETE FROM team_codes WHERE team_id=\"MIL\" AND league=\"AL\""
run_command(c_delete_duplicate)


# In[32]:


# Populating the normalized team table
c_pop_team = '''
INSERT INTO team
SELECT 
    team_id,
    league,
    city,
    nickname,
    franch_id
FROM team_codes'''

run_command(c_pop_team)


# In[33]:


# Verifying 
q_team_check = "SELECT * FROM team"
run_query(q_team_check)


# In[34]:


# Creating empty table for game with desired structure
c_create_game = '''
CREATE TABLE game (
game_id TEXT PRIMARY KEY,
date TEXT,
number_of_game INTEGER,
park_id TEXT,
length_outs INTEGER,
day TEXT,
completion TEXT,
forfeit TEXT, 
protest TEXT,
attendance INTEGER,
length_minutes INTEGER,
additional_info TEXT,
acquisition_info TEXT,
FOREIGN KEY (park_id) REFERENCES park(park_id));'''
    
run_command(c_create_game)


# In[35]:


# Populating the normalized game table 
c_pop_game = '''
INSERT INTO game
SELECT game_id,
date,
number_of_game,
park_id,
length_outs,
day_of_week,
completion,
forefeit,
protest,
attendance,
length_minutes,
additional_info,
acquisition_info
FROM game_log'''

run_command(c_pop_game)


# In[36]:


# Verifying 
q_game_check = "SELECT * FROM game LIMIT 5"
run_query(q_game_check)


# In[37]:


q_game_log = '''SELECT sql FROM sqlite_master 
WHERE name = "game_log" AND type = "table" '''
game_log_extract = run_query(q_game_log)


# In[38]:


game_log_extract


# In[39]:


# Creating the team_appearance table
c_team_app_1 = """
CREATE TABLE IF NOT EXISTS team_appearance (
    team_id TEXT,
    game_id TEXT,
    home BOOLEAN,
    league_id TEXT,
    score INTEGER,
    line_score TEXT,
    at_bats INTEGER,
    hits INTEGER,
    doubles INTEGER,
    triples INTEGER,
    homeruns INTEGER,
    rbi INTEGER,
    sacrifice_hits INTEGER,
    sacrifice_flies INTEGER,
    hit_by_pitch INTEGER,
    walks INTEGER,
    intentional_walks INTEGER,
    strikeouts INTEGER,
    stolen_bases INTEGER,
    caught_stealing INTEGER,
    grounded_into_double INTEGER,
    first_catcher_interference INTEGER,
    left_on_base INTEGER,
    pitchers_used INTEGER,
    individual_earned_runs INTEGER,
    team_earned_runs INTEGER,
    wild_pitches INTEGER,
    balks INTEGER,
    putouts INTEGER,
    assists INTEGER,
    errors INTEGER,
    passed_balls INTEGER,
    double_plays INTEGER,
    triple_plays INTEGER,
    PRIMARY KEY (team_id, game_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);
"""

run_command(c_team_app_1)

c_team_app_2 = """
INSERT OR IGNORE INTO team_appearance
    SELECT
        h_name,
        game_id,
        1 AS home,
        h_league,
        h_score,
        h_line_score,
        h_at_bats,
        h_hits,
        h_doubles,
        h_triples,
        h_homeruns,
        h_rbi,
        h_sacrifice_hits,
        h_sacrifice_flies,
        h_hit_by_pitch,
        h_walks,
        h_intentional_walks,
        h_strikeouts,
        h_stolen_bases,
        h_caught_stealing,
        h_grounded_into_double,
        h_first_catcher_interference,
        h_left_on_base,
        h_pitchers_used,
        h_individual_earned_runs,
        h_team_earned_runs,
        h_wild_pitches,
        h_balks,
        h_putouts,
        h_assists,
        h_errors,
        h_passed_balls,
        h_double_plays,
        h_triple_plays
    FROM game_log

UNION

    SELECT    
        v_name,
        game_id,
        0 AS home,
        v_league,
        v_score,
        v_line_score,
        v_at_bats,
        v_hits,
        v_doubles,
        v_triples,
        v_homeruns,
        v_rbi,
        v_sacrifice_hits,
        v_sacrifice_flies,
        v_hit_by_pitch,
        v_walks,
        v_intentional_walks,
        v_strikeouts,
        v_stolen_bases,
        v_caught_stealing,
        v_grounded_into_double,
        v_first_catcher_interference,
        v_left_on_base,
        v_pitchers_used,
        v_individual_earned_runs,
        v_team_earned_runs,
        v_wild_pitches,
        v_balks,
        v_putouts,
        v_assists,
        v_errors,
        v_passed_balls,
        v_double_plays,
        v_triple_plays
    from game_log;
"""

run_command(c_team_app_2)

# Verifying the data was inserted correctly 
q_team_app = """
SELECT * FROM team_appearance
WHERE game_id = (
                 SELECT MIN(game_id) from game
                )
   OR game_id = (
                 SELECT MAX(game_id) from game
                )
ORDER By game_id, home;
"""

run_query(q_team_app)


# In[40]:


# Creating the person_appearance table
c_drop = "DROP TABLE IF EXISTS person_appearance"

run_command(c_drop)

c_person_app_create = """
CREATE TABLE person_appearance (
    appearance_id INTEGER PRIMARY KEY,
    person_id TEXT,
    team_id TEXT,
    game_id TEXT,
    appearance_type_id,
    FOREIGN KEY (person_id) REFERENCES person(person_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (appearance_type_id) REFERENCES appearance_type(appearance_type_id)
);
"""

c_person_app_fill = """
INSERT OR IGNORE INTO person_appearance (
    game_id,
    team_id,
    person_id,
    appearance_type_id
) 
    SELECT
        game_id,
        NULL,
        hp_umpire_id,
        "UHP"
    FROM game_log
    WHERE hp_umpire_id IS NOT NULL    

UNION

    SELECT
        game_id,
        NULL,
        [1b_umpire_id],
        "U1B"
    FROM game_log
    WHERE "1b_umpire_id" IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        [2b_umpire_id],
        "U2B"
    FROM game_log
    WHERE [2b_umpire_id] IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        [3b_umpire_id],
        "U3B"
    FROM game_log
    WHERE [3b_umpire_id] IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        lf_umpire_id,
        "ULF"
    FROM game_log
    WHERE lf_umpire_id IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        rf_umpire_id,
        "URF"
    FROM game_log
    WHERE rf_umpire_id IS NOT NULL

UNION

    SELECT
        game_id,
        v_name,
        v_manager_id,
        "MM"
    FROM game_log
    WHERE v_manager_id IS NOT NULL

UNION

    SELECT
        game_id,
        h_name,
        h_manager_id,
        "MM"
    FROM game_log
    WHERE h_manager_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        winning_pitcher_id,
        "AWP"
    FROM game_log
    WHERE winning_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score < v_score THEN h_name
            ELSE v_name
            END,
        losing_pitcher_id,
        "ALP"
    FROM game_log
    WHERE losing_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        saving_pitcher_id,
        "ASP"
    FROM game_log
    WHERE saving_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        winning_rbi_batter_id,
        "AWB"
    FROM game_log
    WHERE winning_rbi_batter_id IS NOT NULL

UNION

    SELECT
        game_id,
        v_name,
        v_starting_pitcher_id,
        "PSP"
    FROM game_log
    WHERE v_starting_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        h_name,
        h_starting_pitcher_id,
        "PSP"
    FROM game_log
    WHERE h_starting_pitcher_id IS NOT NULL;
"""

template = """
INSERT INTO person_appearance (
    game_id,
    team_id,
    person_id,
    appearance_type_id
) 
    SELECT
        game_id,
        {hv}_name,
        {hv}_player_{num}_id,
        "O{num}"
    FROM game_log
    WHERE {hv}_player_{num}_id IS NOT NULL

UNION

    SELECT
        game_id,
        {hv}_name,
        {hv}_player_{num}_id,
        "D" || CAST({hv}_player_{num}_def_pos AS INT)
    FROM game_log
    WHERE {hv}_player_{num}_id IS NOT NULL;
"""

run_command(c_person_app_create)
run_command(c_person_app_fill)

# Iterating through the columns to create the query
for hv in ["h","v"]:
    for num in range(1,10):
        query_vars = {
            "hv": hv,
            "num": num
        }
        run_command(template.format(**query_vars))


# In[41]:


# Verifying Data
print(run_query("SELECT COUNT(DISTINCT game_id) games_game FROM game"))
print(run_query("SELECT COUNT(DISTINCT game_id) games_person_appearance FROM person_appearance"))

q_appearence = """
SELECT
    pa.*,
    at.name,
    at.category
FROM person_appearance pa
INNER JOIN appearance_type at on at.appearance_type_id = pa.appearance_type_id
WHERE PA.game_id = (
                   SELECT max(game_id)
                    FROM person_appearance
                   )
ORDER BY team_id, appearance_type_id
"""

run_query(q_appearence)


# In[43]:


def show_tables():
    q = '''
    SELECT
        name,
        type
    FROM sqlite_master
    WHERE type IN ("table","view");
    '''
    return run_query(q)

show_tables()


# In[45]:


# Dropping tables that have not been normalized 
c_drop_game_log = "DROP TABLE IF EXISTS game_log"
c_drop_park_codes = "DROP TABLE IF EXISTS park_codes"
c_drop_team_codes = "DROP TABLE IF EXISTS team_codes"
c_drop_person_codes = "DROP TABLE IF EXISTS person_codes"

run_command(c_drop_game_log)
run_command(c_drop_park_codes)
run_command(c_drop_team_codes)
run_command(c_drop_person_codes)

show_tables()


# ## Project Overview
# 
# - Import CSV data into a database.
# - Design a normalized schema for a large, predominantly single table data set.
# - Create tables that match the schema design.
# - Migrate data from unnormalized tables into our normalized tables.
