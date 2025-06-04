from src.utils import get_driver
import json


def push_to_neo4j(json_data:list, detail_file:list, concept_file:list)->None:
    driver = get_driver()

    with driver.session() as session:
        for item in json_data:
            phenotype_name = item.get("Phenotypes")
            session.run("""
                CREATE (p:Phenotype {id:$row.id}) 
                SET p += $row
                SET p.name = $name
                REMOVE p.Phenotypes
            """, name=phenotype_name,row = item)
            pid_sources = {
                        'HDRUK': item.get("hdruk_PID"),
                        'PHEKB': item.get("phekb_PID"),
                        'CPRD': item.get("cprd_PID"),
                        'Sentinel': item.get("Sentinel_PID"),
                        'OHDSI': item.get("ohdsi_PID"),
                    }
            # print(pid_sources)

            for source, pid_string in pid_sources.items():
                if pid_string:
                    # print(source)
                    website_pids = [pid.strip() for pid in pid_string.split(",") if pid.strip()]
                    session.run("""
                                CREATE  (w:Website {name: $name, pid: $pids})
                                WITH w
                                MATCH (p:Phenotype {id:$row.id})
                                MERGE (p)-[:HAS_INSTANCE]->(w)
                                    """,name = source,pids = website_pids,row = item)
                    
                    for pid in website_pids:
                        detail_row = next(detail_dictionary for detail_dictionary in detail_file if pid == detail_dictionary['PID'])
                        # print(pid)
                        for key,value in detail_row.items():
                            if isinstance(value,dict):
                                detail_row[key] = json.dumps(value)
                            elif isinstance(value,list):
                                if all(isinstance(subitem, dict) for subitem in value):
                                    detail_row[key] = json.dumps([json.dumps(item) for item in value])
                                else:
                                    detail_row[key] = value if value is not None else []
                            elif value is None or value == 'NA' or value == 'NO_VALUE':
                                detail_row[key] = 'Unknown value'
                        session.run("""
                                CREATE (d:Detail {PID:$detail_row.PID})
                                SET d += $detail_row
                                WITH d
                                MATCH (p:Phenotype {id:$row.id}) 
                                MATCH (w:Website {name:$name})
                                MATCH (p)-[:HAS_INSTANCE]->(w)
                                MERGE (w)-[:HAS_DETAIL]->(d)
                                """,detail_row = detail_row,row = item,name = source)
                        concept_row = [concept_dictionary for concept_dictionary in concept_file if pid in concept_dictionary['PIDs']] 
                        if len(concept_row)<1:
                            continue
                    
                        for concept in concept_row:
                            for key in list(concept.keys()):
                                value = concept[key]
                                if isinstance(value, (dict, list)):
                                    concept[key] = json.dumps(value)
                            session.run("""
                                        CREATE (c:Concept {CID:$concept.CID})
                                        SET c += $concept
                                        WITH c
                                        MATCH (p:Phenotype {id:$row.id}) 
                                        MATCH (w:Website {name:$name})
                                        MATCH (d:Detail {PID:$pid})
                                        MATCH (p)-[:HAS_INSTANCE]->(w)-[:HAS_DETAIL]->(d)
                                        MERGE (d)-[:HAS_CONCEPT]->(c)
                                        """,concept = concept,row = item,name = source,pid = pid)
    
    return "Phenomix data added to Neo4J.."

