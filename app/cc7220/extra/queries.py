import json
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
import logging

queries_log = logging.getLogger('QUERIES')


class Queries:
    @staticmethod
    def query(query=None, json_path=None, log="", already_asked=False, limit=None):
        if limit is not None:
            query += "LIMIT"+str(limit)
        if not already_asked:
            res = return_sparql_query_results(query)
            res = res['results']['bindings']
            queryset = json.dumps(res, sort_keys=True, indent=2)
            f = open(json_path, 'w')
            f.write(queryset)
            queries_log.warn(f"{queries_log.name}: {log}")
        else:
            query = open(json_path, 'r')
            res = json.load(query)
            queries_log.warn(f"{queries_log.name}: {log}")
        return res

    # CANTIDAD DE CIENTÍFICOS POR PAIS
    ccbc = """
    # Cantidad de científicos agrupados por países
    #notas:Rusia-URSS muchas veces, como primera ocupación scientist (no se pide sub clase por que la querrá muere)
    SELECT DISTINCT ?country (COUNT(distinct ?human) as ?number)
    WHERE {
      ?human wdt:P31 wd:Q5;
             (wdt:P106) wd:Q901 ;
             wdt:P27 ?nationality ;
             rdfs:label ?name .
      ?nationality rdfs:label ?country .
      FILTER (lang(?name)="en") 
      FILTER (lang(?country)="en")
      }
    GROUP BY ?country
    ORDER BY DESC(?number)
    
    """

    ccbc_asked = False

    @staticmethod
    def get_ccbc(limit=None):
        res = Queries.query(query=Queries.ccbc,
                            json_path="cc7220/templates/json/q1.json",
                            log="ccbc retrieved" if Queries.ccbc_asked else "ccbc asked",
                            already_asked=Queries.ccbc_asked,
                            limit=limit)
        Queries.ccbc_asked = True
        return res

    # Mayores causas de muerte de los científicos = mcmc
    mcmc = """
    SELECT ?causes (count(?human) as ?humans) 
    WHERE {
      ?human wdt:P31 wd:Q5;
             (wdt:P106|wdt:P279*) wd:Q901 ;
             wdt:P1196 ?mannerOfDeath;
             wdt:P509 ?causesOfDeath;
             rdfs:label ?name .
      ?causesOfDeath rdfs:label ?causes.
      ?mannerOfDeath rdfs:label ?manner.
      FILTER (lang(?name)="en")
      FILTER (lang(?causes)="en")
      FILTER (lang(?manner)="en")
      }
    GROUP BY ?causes
    ORDER BY DESC(?humans)
    
    """

    mcmc_asked = False

    @staticmethod
    def get_mcmc(limit=None):
        res = Queries.query(query=Queries.mcmc,
                            json_path="cc7220/templates/json/q2.json",
                            log="mcmc retrieved" if Queries.mcmc_asked else "mcmc asked",
                            already_asked=Queries.mcmc_asked,
                            limit=limit)
        Queries.mcmc_asked = True
        return res

    # Lista de ocupaciones científicas
    loc = """
    SELECT DISTINCT ?scientific_occupations
    WHERE {
      ?occupation wdt:P31 wd:Q28640;
                  (wdt:P106|wdt:P279*) wd:Q901;
                  rdfs:label ?scientific_occupations .
      FILTER(lang(?scientific_occupations)="en") .
      }
    ORDER BY ?scientific_occupations
    """

    loc_asked = False

    @staticmethod
    def get_loc():
        res = Queries.query(query=Queries.loc,
                            json_path="cc7220/templates/json/q3.json",
                            log="loc retrieved" if Queries.loc_asked else "loc asked",
                            already_asked=Queries.loc_asked)
        Queries.loc_asked = True
        return res

    # cantidad de cientificos por campo de estudio
    ccce = """SELECT ?subjectname (COUNT(?scientist) as ?count)
            WHERE {
            ?scientist  wdt:P31 wd:Q5;
            (wdt:P106|wdt:P279*) wd:Q901 ;
            wdt:P800 ?work;
            wdt:P101 ?field .
            ?field rdfs:label ?fieldname .
            ?work wdt:P921 ?subject .
            ?subject wdt:P31 wd:Q11862829 ;
            rdfs:label ?subjectname .
                FILTER (lang(?subjectname)="en") .
            FILTER (lang(?fieldname)="en") .
            }
            group by ?subjectname
            order by desc(?count)
            
            """

    ccce_asked = False

    @staticmethod
    def get_ccce(limit=None):
        res = Queries.query(query=Queries.ccce,
                            json_path="cc7220/templates/json/q4.json",
                            log="ccce retrieved" if Queries.ccce_asked else "ccce asked",
                            already_asked=Queries.ccce_asked,
                            limit=limit)
        Queries.ccce_asked = True
        return res

    #paises donde NACIERON los cientificos
    pdnc = """
    SELECT ?country (count(?human) as ?humans)
    WHERE {
    ?human wdt:P31 wd:Q5;
    (wdt:P106|wdt:P279*) wd:Q901 ;
    wdt:P19 ?placeOfBirth;
    rdfs:label ?name .
    ?placeOfBirth wdt:P17 ?c.
    ?c rdfs:label ?country.
        FILTER (lang(?name)="en")
    FILTER (lang(?country)="en")
    }
    GROUP BY ?country
    ORDER BY DESC(?humans)
    
    """

    pdnc_asked = False

    @staticmethod
    def get_pdnc(limit=None):
        res = Queries.query(query=Queries.pdnc,
                            json_path="cc7220/templates/json/q5.json",
                            log="pdnc retrieved" if Queries.pdnc_asked else "pdnc asked",
                            already_asked=Queries.pdnc_asked,
                            limit=limit)
        Queries.pdnc_asked = True
        return res

    # científicos en guerras
    ceg = """
    SELECT DISTINCT ?warname ?countryname (GROUP_CONCAT (DISTINCT ?name; SEPARATOR=", ") as ?scientists)
    WHERE {
      ?scientist wdt:P106 wd:Q901 ;
                 wdt:P607 ?war;
                 wdt:P27 ?country ;
          rdfs:label ?name .
      ?war rdfs:label ?warname .
      ?country rdfs:label ?countryname .
      FILTER (lang(?name)="en") .
      FILTER (lang(?warname)="en") .
      FILTER (lang(?countryname)="en") .
      }
    GROUP BY ?warname ?countryname
    ORDER BY ?warname
    """

    ceg_asked = False

    @staticmethod
    def get_ceg(limit=None):
        res = Queries.query(query=Queries.ceg,
                            json_path="cc7220/templates/json/q6.json",
                            log="ceg retrieved" if Queries.ceg_asked else "ceg asked",
                            already_asked=Queries.ceg_asked,
                            limit=limit)
        Queries.ceg_asked = True
        return res
