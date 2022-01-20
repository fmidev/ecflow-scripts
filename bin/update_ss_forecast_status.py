#!/usr/bin/env python3

import sys
import datetime
import psycopg2
import psycopg2.extras
import os
import argparse

from pytz import timezone

cur = None
conn = None

def parse_command_line():
    def valid_time(x):
        try:
            return datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            raise argparse.ArgumentTypeError(e)

    parser = argparse.ArgumentParser()
    parser.add_argument("--producer_id","-r", action='store', type=int, required=True)
    parser.add_argument("--analysis_time","-a", action='store', type=valid_time, required=True)
    parser.add_argument("--version", action='store', type=int, default=1)
    parser.add_argument("--status","-s", action='store', type=str, required=True)
    parser.add_argument("--status_time","-t", action='store', type=valid_time, default=datetime.datetime.now())
    parser.add_argument("--geometry_id", action='store', default=None)
    parser.add_argument("--host", action="store", type=str, default="radondb.fmi.fi", help="Database hostname")
    parser.add_argument("--port", action="store", type=int, default=5432, help="Database port")
    parser.add_argument("--database", action="store", type=str, default="radon", help="Database name")
    parser.add_argument("--user", action="store", type=str, default="wetodb", help="Database username")

    args = parser.parse_args()

    allowed_statuses = [ 'READY' ]

    if args.status not in allowed_statuses:
        raise Exception('{} is not one of allowed statuses: {}'.format(args.status, allowed_statuses))
    return args


def update_ss_status(args, conn):
    cur = conn.cursor()
    query = 'INSERT INTO ss_forecast_status (producer_id, analysis_time, geometry_id, version, status, status_time) VALUES (%s, %s, %s, %s, %s, %s)'

    try:
        cur.execute(query, (args.producer_id, args.analysis_time, args.geometry_id, args.version, args.status, args.status_time))
    except psycopg2.IntegrityError as e:
        print(e)
        print("Use a different version than '{}' if this is a second run of the forecast".format(args.version))
        sys.exit(1)
    except psycopg2.InternalError as e:
        print(e)
        print("Use a different version than '{}' if this is a second run of the forecast, or specify geometry id".format(args.version))
        sys.exit(1)

    print("Inserted status '{}' for producer {} analysis time {} geometry {} version {}".format(args.status, args.producer_id, args.analysis_time, args.geometry_id, args.version))


def connect(args):
    print("Connecting to database {} at host {}:{}".format(args.database, args.host, args.port))

    password = None

    try:
        password = os.environ["RADON_{}_PASSWORD".format(args.user.upper())]
    except:
        print("password should be given with env variable RADON_{}_PASSWORD".format(args.user.upper()))
        sys.exit(1)

    dsn = "user={} password={} host={} dbname={} port={}".format(args.user, password, args.host, args.database, args.port)
    conn = psycopg2.connect(dsn)

    conn.autocommit = 0

    return conn

def main():
    global opts, args

    args = parse_command_line()

    conn = connect(args)
    update_ss_status(args, conn)

    conn.commit()

if __name__ == "__main__":
    main()
