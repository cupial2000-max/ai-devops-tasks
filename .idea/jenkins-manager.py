
import os
import argparse
import requests
from requests.auth import HTTPBasicAuth

# Konfiguracja połączenia z Jenkins
JENKINS_URL = os.getenv("JENKINS_URL", "http://localhost:8080").rstrip("/")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

# Sesja HTTP z autoryzacją
session = requests.Session()

if JENKINS_USER and JENKINS_TOKEN:
    session.auth = HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN)


def make_request(url, method="GET"):
    """Wykonuje zapytanie do Jenkins API."""
    try:
        response = session.request(
            method,
            url,
            timeout=15
        )
        response.raise_for_status()
        return response

    except requests.exceptions.Timeout:
        print("Blad: Przekroczono czas oczekiwania na odpowiedz Jenkins.")
    except requests.exceptions.ConnectionError:
        print("Blad: Nie mozna polaczyc sie z Jenkins.")
    except requests.exceptions.HTTPError as error:
        print(f"Blad HTTP: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Blad zapytania: {error}")

    return None


def list_jobs():
    """Wyswietla wszystkie zadania Jenkins."""
    url = f"{JENKINS_URL}/api/json?tree=jobs[name,color,url]"
    response = make_request(url)

    if response is None:
        return

    try:
        jobs = response.json().get("jobs", [])

        if not jobs:
            print("Nie znaleziono zadnych zadan.")
            return

        print("\nLista zadan Jenkins:")
        for job in jobs:
            print(f"- {job['name']} | Status: {job['color']}")

    except (ValueError, KeyError) as error:
        print(f"Blad odczytu odpowiedzi API: {error}")


def check_status(job_name):
    """Sprawdza status ostatniego buildu wybranego zadania."""
    url = (
        f"{JENKINS_URL}/job/{job_name}/api/json"
        "?tree=lastBuild[number,result,building,timestamp]"
    )

    response = make_request(url)

    if response is None:
        return

    try:
        data = response.json()
        build = data.get("lastBuild")

        if not build:
            print(f"Zadanie '{job_name}' nie ma jeszcze zadnego buildu.")
            return

        if build.get("building"):
            status = "BUILD W TRAKCIE"
        else:
            status = build.get("result") or "BRAK WYNIKU"

        print(f"\nZadanie: {job_name}")
        print(f"Numer buildu: {build['number']}")
        print(f"Status: {status}")

    except (ValueError, KeyError) as error:
        print(f"Blad odczytu odpowiedzi API: {error}")


def run_job(job_name):
    """Uruchamia wybrane zadanie Jenkins."""
    url = f"{JENKINS_URL}/job/{job_name}/build"

    response = make_request(url, method="POST")

    if response is not None:
        print(f"Zadanie '{job_name}' zostalo wyslane do uruchomienia.")
        print(f"Kod odpowiedzi HTTP: {response.status_code}")


def main():
    parser = argparse.ArgumentParser(
        description="Skrypt do zarzadzania zadaniami Jenkins"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    subparsers.add_parser("list", help="Wyswietla wszystkie zadania")

    status_parser = subparsers.add_parser(
        "status",
        help="Sprawdza status ostatniego buildu"
    )
    status_parser.add_argument("job_name")

    run_parser = subparsers.add_parser(
        "run",
        help="Uruchamia wybrane zadanie"
    )
    run_parser.add_argument("job_name")

    args = parser.parse_args()

    if not JENKINS_USER or not JENKINS_TOKEN:
        print("Blad: Ustaw zmienne JENKINS_USER i JENKINS_TOKEN.")
        return

    if args.command == "list":
        list_jobs()
    elif args.command == "status":
        check_status(args.job_name)
    elif args.command == "run":
        run_job(args.job_name)


if __name__ == "__main__":
    main()
