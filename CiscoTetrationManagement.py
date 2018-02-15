#! /usr/bin/env python
"""Cisco Tetration Analytics Python script."""

import argparse
import json
import csv
from tetpyclient import RestClient
from termcolor import colored

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# https://www.twitter.com/mrlesmithjr
# http://mrlesmithjr.com

EXAMPLES = """
View application scopes
-----------------------
python CiscoTetrationManagement.py get_app_scopes \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json

View application scope by name
------------------------------
python CiscoTetrationManagement.py get_app_scope \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appscopeshortname "Demo"

View application scope by id
----------------------------
python CiscoTetrationManagement.py get_app_scope \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appscopeid 599f4f35755f0237896ce9cf

View applications
-----------------
python CiscoTetrationManagement.py get_apps \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json

View a specific application by using app id
-------------------------------------------
python CiscoTetrationManagement.py get_app \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appid 59cdc1e7755f0225066ce9d4

View a specific application by using app name and appscopeid
------------------------------------------------------------
python CiscoTetrationManagement.py get_app \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appname "Tenant2" --appscopeid 599f4f35755f0237896ce9cf

Create an application by appscopeid
-----------------------------------
python CiscoTetrationManagement.py create_app \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appname "Test App" --appdescription "Test App Using API" \
--appscopeprimary False --appscopeid xxxxxx

Create an application by appscopeshortname
------------------------------------------
python CiscoTetrationManagement.py create_app \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appname "Test App" --appdescription "Test App Using API" \
--appscopeprimary False --appscopeshortname "xxxxx"

View an application clusters
----------------------------
python CiscoTetrationManagement.py get_app_clusters \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appid 59cdc1e7755f0225066ce9d4

Delete an application
---------------------
python CiscoTetrationManagement.py delete_app \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--appid 59cdc1e7755f0225066ce9d4

Create users with CSV file as input
-----------------------------------
python CiscoTetrationManagement.py add_users \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--readcsv users.csv

Get a sensor
------------
python CiscoTetrationManagement.py get_sensor \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--hostname server001

Delete a sensor
---------------
python CiscoTetrationManagement.py delete_sensor \
--apiendpoint https://172.16.5.4 --credsfile api_credentials.json \
--hostname server001 --ip 172.27.2.166
"""


class Tetration(object):
    """Main execution."""

    def __init__(self):
        """Setup initial call."""
        self.read_cli_args()
        self.auth()
        self.decide_action()

    def auth(self):
        """Setup Auth."""
        if self.args.credsfile is not None:
            self.restclient = (RestClient(self.args.apiendpoint,
                                          credentials_file=self.args.credsfile,
                                          verify=False))

    def decide_action(self):
        """
        Determine action.

        Based on action passed determine which action to take.
        """
        if self.args.action == "add_user_roles":
            self.add_user_roles()
        if self.args.action == "add_user_to_role":
            self.add_user_to_role()
        if self.args.action == "add_users":
            self.add_users()
        if self.args.action == "create_app":
            self.create_app()
        if self.args.action == "create_app_scope":
            self.create_app_scope()
        if self.args.action == "delete_app":
            self.delete_app()
        if self.args.action == "delete_sensor":
            self.delete_sensor()
        if self.args.action == "delete_users":
            self.delete_users()
        if self.args.action == "get_app":
            self.get_app()
        if self.args.action == "get_app_clusters":
            self.get_app_clusters()
        if self.args.action == "get_apps":
            self.get_apps()
        # if self.args.action == "get_app_scope_ids":
        #     self.get_app_scope_ids()
        if self.args.action == "get_app_scope":
            self.get_app_scope()
        if self.args.action == "get_app_scopes":
            self.get_app_scopes()
        if self.args.action == "get_flow_dimensions":
            self.get_flow_dimensions()
        if self.args.action == "get_flow_metrics":
            self.get_flow_metrics()
        if self.args.action == "get_inventory_dimensions":
            self.get_inventory_dimensions()
        if self.args.action == "get_inventory_filters":
            self.get_inventory_filters()
        if self.args.action == "get_sensor":
            self.get_sensor()
        if self.args.action == "get_sensors":
            self.get_sensors()
        if self.args.action == "get_switches":
            self.get_switches()
        if self.args.action == "get_user":
            self.get_user()
        if self.args.action == "get_user_roles":
            self.get_user_roles()
        if self.args.action == "get_users":
            self.get_users()
        if self.args.action == "remove_user_from_role":
            self.remove_user_from_role()

    def add_user_roles(self):
        """Add roles."""
        self.get_user_roles()
        if self.args.readcsv is not None:
            try:
                f = open(self.args.readcsv)
                csv_f = csv.reader(f)
                next(csv_f, None)  # skip headers
                for row in csv_f:
                    self.args.userrole = row[0]
                    self.args.userroledescription = row[1]
                    if self.args.userrole not in self.roles:
                        if not self.args.userroledescription:
                            self.args.userroledescription = self.args.userrole
                        req_payload = {
                            "name": self.args.userrole,
                            "description": self.args.userroledescription
                        }
                        resp = self.restclient.post(
                            '/roles', json_body=json.dumps(req_payload)
                        )
                        if resp.status_code == 200:
                            print colored('Role: \"%s\" successfully added'
                                          % self.args.userrole, 'yellow')

                    # Manage scope capabilities to assign to roles
                    # Need to cleanup code a bit and maybe move around as this
                    # may not be completely optimal
                    if row[2]:
                        self.args.appscopeshortname = row[2]
                        self.get_app_scope()
                        if self.app_scope_id is not None:
                            if row[3]:
                                resp = self.restclient.get(
                                    '/roles'
                                )
                                if resp.status_code == 200:
                                    python_data = json.loads(resp.text)
                                    for key in python_data:
                                        if key['name'] == row[0]:
                                            req_payload = {
                                                "app_scope_id":
                                                self.app_scope_id,
                                                "ability": row[3]
                                            }
                                            role_id = key['id']
                                            resp = self.restclient.post(
                                                '/roles/%s/capabilities'
                                                % role_id,
                                                json_body=json.dumps(
                                                    req_payload)
                                            )
                                            if resp.status_code == 200:
                                                print colored(
                                                    'Capability successfully assigned',
                                                    'yellow')
                                            if resp.status_code == 400:
                                                print colored(
                                                    'Capablity already assigned',
                                                    'yellow')

                    else:
                        print colored('User role: \"%s\" already exists'
                                      % self.args.userrole,
                                      'yellow')
            finally:
                f.close()
        else:
            if self.args.userrole not in self.roles:
                if self.args.userroledescription is None:
                    self.args.userroledescription = self.args.userrole
                req_payload = {
                    "name": self.args.userrole,
                    "description": self.args.userroledescription
                }
                resp = self.restclient.post(
                    '/roles', json_body=json.dumps(req_payload)
                )
                if resp.status_code == 200:
                    print colored('Role: \"%s\" successfully added'
                                  % self.args.userrole, 'yellow')
            else:
                print colored('User role: \"%s\" already exists'
                              % self.args.userrole,
                              'yellow')

    def add_user_to_role(self):
        """Add A User To A role."""
        # NEED to add ability defined more than one role ####
        self.get_user_roles()
        self.get_user()
        if self.user_role_id is not None:
            if self.user_role_id not in self.user_role_ids:
                req_payload = {
                    "role_id": self.user_role_id
                }
                endpoint = '/users/%s/add_role' % self.user_id
                resp = self.restclient.put(
                    '%s' % endpoint, json_body=json.dumps(req_payload))
                if resp.status_code == 200:
                    print colored('User successfully assigned to role...',
                                  'yellow')
            else:
                print colored('User already assigned role...Skipping',
                              'yellow')
        else:
            print colored('Role does not exist and user not added to role: ',
                          'yellow') + self.args.userrole

    def add_users(self):
        """Add Users."""
        if self.args.readcsv is not None:
            try:
                f = open(self.args.readcsv)
                csv_f = csv.reader(f)
                next(csv_f, None)  # skip headers
                for row in csv_f:
                    self.args.useremail = row[0]
                    self.args.userfirstname = row[1]
                    self.args.userlastname = row[2]
                    self.get_user()
                    if self.user_id is not None:
                        print colored('User already exists with ID: ',
                                      'yellow') + self.user_id
                    else:
                        req_payload = {
                            "first_name": self.args.userfirstname,
                            "last_name": self.args.userlastname,
                            "email": self.args.useremail
                        }
                        resp = self.restclient.post(
                            '/users', json_body=json.dumps(req_payload))
                        # if resp.status_code == 200:
                        #     self.get_user()
                        #     print colored('User successfully created with ID: ',
                        #                   'yellow') + self.user_id
                    self.get_user()
                    if row[3]:
                        for role in row[3].split(','):
                            self.args.userrole = role
                            # self.args.add_user_roles()
                            self.add_user_to_role()
            finally:
                f.close()
        else:
            self.get_user()
            if self.user_id is not None:
                print colored('User already exists with ID: ',
                              'yellow') + self.user_id
            else:
                req_payload = {
                    "first_name": self.args.userfirstname,
                    "last_name": self.args.userlastname,
                    "email": self.args.useremail
                }
                resp = self.restclient.post(
                    '/users', json_body=json.dumps(req_payload))
                if resp.status_code == 200:
                    self.get_user()
                    print colored('User successfully created with ID: ',
                                  'yellow') + self.user_id
            if self.args.userrole is not None:
                self.add_user_to_role()

    def create_app(self):
        """Create An Application."""
        self.get_apps()
        if self.args.appdescription is None:
            appdescription = ""
        else:
            appdescription = self.args.appdescription
        if self.app_name is None:
            req_payload = {
                "app_scope_id": self.app_scope_id,
                "name": self.args.appname,
                "description": appdescription,
                "primary": self.args.appscopeprimary
            }
            resp = self.restclient.post(
                '/applications', json_body=json.dumps(req_payload))
            if resp.status_code == 200:
                self.get_apps()
                self.get_app()
                print colored('Application successfully created....'
                              'Details above...', 'yellow')
        else:
            self.get_app()
            print colored('Application already exists....Details above...',
                          'yellow')

    def delete_app(self):
        """Delete An Application."""
        self.get_apps()
        if self.app_name is not None:
            resp = self.restclient.delete(
                '/applications/%s' % self.args.appid)
            if resp.status_code == 200:
                print colored('Application with id: %s'
                              % self.args.appid,
                              'yellow') + " successfully deleted..."
        else:
            print colored('Application with id: %s'
                          % self.args.appid, 'yellow') + " not found..."

    def delete_sensor(self):
        """Delete A Sensor."""
        self.get_sensors()
        if self._sensor_info != {}:
            if self.args.ip in self._sensor_info['ips']:
                for _uuid in self._sensor_info['uuids']:
                    resp = self.restclient.delete(
                        '/sensors/%s' % _uuid
                    )
                    print resp
                    if resp.status_code == 204:
                        print colored(
                            'Sensor %s with uuid: %s has been deleted'
                            % (self.args.hostname, _uuid), 'yellow')

    def delete_users(self):
        """Delete users."""
        if self.args.readcsv is not None:
            try:
                f = open(self.args.readcsv)
                csv_f = csv.reader(f)
                next(csv_f, None)  # skip headers
                for row in csv_f:
                    self.args.useremail = row[0]
                    self.args.userfirstname = row[1]
                    self.args.userlastname = row[2]
                    self.get_user()
                    if self.user_id is not None:
                        resp = self.restclient.delete(
                            '/users/%s' % self.user_id)
                        if resp.status_code == 200:
                            print colored(
                                'User %s %s %s with id: %s was deleted'
                                % (self.args.userfirstname,
                                   self.args.userlastname,
                                   self.args.useremail,
                                   self.user_id),
                                'yellow')
                    else:
                        print colored('User does not exist', 'yellow')
            finally:
                f.close()
        else:
            self.get_user()
            if self.user_id is not None:
                resp = self.restclient.delete(
                    '/users/%s' % self.user_id)
                if resp.status_code == 200:
                    print colored(
                        'User %s %s %s with id: %s was deleted'
                        % (self.args.userfirstname,
                           self.args.userlastname,
                           self.args.useremail,
                           self.user_id),
                        'yellow')
            else:
                print colored('User does not exist', 'yellow')

    # Need to finish this functionality. Currently only reads in a CSV...
    def create_app_scope(self):
        """Create An Application Scope."""
        if self.args.readcsv is not None:
            try:
                f = open(self.args.readcsv)
                csv_f = csv.reader(f)
                next(csv_f, None)  # skip headers
                for row in csv_f:
                    # We first capture the parent scope id to create scope under
                    parent_scope_shortname = row[4]
                    self.args.appscopeshortname = parent_scope_shortname
                    self.get_app_scope()
                    parent_scope_id = self.app_scope_id
                    #
                    # We now capture the new scope to create
                    self.args.appscopeshortname = row[0]
                    self.get_app_scope()
                    if (self.app_scope_id is None and
                            parent_scope_id is not None):
                        req_payload = {
                            "short_name": row[0],
                            "short_query": {
                                "type": row[2],
                                "field": row[1],
                                "value": row[3]
                            },
                            "parent_app_scope_id": parent_scope_id
                        }
                        resp = self.restclient.post(
                            '/app_scopes', json_body=json.dumps(req_payload))
                        if resp.status_code == 200:
                            print "Successfully created app scope %s" % row[0]
                    else:
                        print "Already exists"

                    # We now need to check for any "Dirty" root scopes in order
                    # to commit the changes.
                    resp = self.restclient.get(
                        '/app_scopes/%s' % parent_scope_id
                    )
                    if resp.status_code == 200:
                        python_data = json.loads(resp.text)
                        if python_data['dirty']:
                            req_payload = {
                                "root_app_scope_id": parent_scope_id
                            }
                            resp = self.restclient.post(
                                '/app_scopes/commit_dirty',
                                json_body=json.dumps(req_payload))
                            if resp.status_code == 201:
                                print colored('Job queued', 'yellow')
            finally:
                f.close()

    def get_app(self):
        """Capture Specific Application."""
        if self.args.action == "create_app":
            resp = self.restclient.get(
                '/applications/%s/details' % self.app_id)
        if self.args.action == "get_app":
            if self.args.appid is not None and self.args.appname is None:
                resp = self.restclient.get(
                    '/applications/%s/details' % self.args.appid)
                if resp.status_code == 404:
                    print colored('Application not found...', 'yellow')
            if self.args.appid is None and self.args.appname is not None:
                self.get_apps()
                if self.app_id is not None:
                    resp = self.restclient.get(
                        '/applications/%s/details' % self.app_id)
                else:
                    print colored('Application does not exist...', 'yellow')
                    return
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            print json.dumps(python_data, indent=4)

    def get_app_clusters(self):
        """Capture Specific Application."""
        resp = self.restclient.get(
            '/applications/%s/details' % self.args.appid
        )
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            _data = {}
            if 'clusters' in python_data:
                _data.update({'Clusters': python_data['clusters']})
                print json.dumps(_data, indent=4)
            else:
                print colored('No clusters found for app!...Run ADM?',
                              'yellow')

    def get_apps(self):
        """Capture Applications."""
        resp = self.restclient.get('/applications')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.action == "create_app":
                if (self.args.appscopeid is not None and
                        self.args.appscopeshortname is None):
                    for key in python_data:
                        if (key['app_scope_id'] == self.args.appscopeid and
                                key['name'] == self.args.appname):
                            self.app_id = key['id']
                            self.app_name = key['name']
                            return
                        else:
                            self.app_name = None
                            self.app_scope_id = self.args.appscopeid
                if (self.args.appscopeid is None and
                        self.args.appscopeshortname is not None):
                    self.get_app_scopes()
                    if self.app_scope_id is not None:
                        for key in python_data:
                            if (key['app_scope_id'] == self.app_scope_id and
                                    key['name'] == self.args.appname):
                                self.app_id = key['id']
                                self.app_name = key['name']
                                return
                            else:
                                self.app_name = None
            if self.args.action == "delete_app":
                for key in python_data:
                    if key['id'] == self.args.appid:
                        self.app_name = key['name']
                        return
                    else:
                        self.app_name = None
                return
            if (self.args.action == "get_app" and
                    self.args.appname is not None and
                    self.args.appscopeid is not None):
                for key in python_data:
                    if (key['name'] == self.args.appname and
                            key['app_scope_id'] == self.args.appscopeid):
                        self.app_id = key['id']
                        return
                    else:
                        self.app_id = None
            else:
                if self.args.savetofile:
                    self.save_results(python_data)
                else:
                    if self.args.action != "create_app":
                        print json.dumps(python_data, indent=4)

    # def get_app_scope_ids(self):
    #     """
    #     Capture Application Scope IDs
    #     """
    #     resp = self.restclient.get('/app_scopes')
    #     if resp.status_code == 200:
    #         python_data = json.loads(resp.text)
    #         data = []
    #         for key in python_data:
    #             item = {}
    #             item.update(
    #                 {"Application Parent Id": key['parent_app_scope_id']})
    #             item.update({"Application Scope Id": key['id']})
    #             item.update({"Application Scope Full Name": key['name']})
    #             item.update({"Application Scope Full Query": key['query']})
    #             item.update(
    #                 {"Application Scope Short Name": key['short_name']})
    #             item.update(
    #                 {"Application Scope Short Query": key['short_query']})
    #             item.update({"Application VRF Id": key['vrf_id']})
    #             data.append(item)
    #         print json.dumps(data, indent=4)
    #         # # print (colored('Scope Name: ', 'yellow') + key['name'] + '  ' +
    #         # #        colored('Parent Id: ', 'yellow') + key['parent_app_scope_id'] + '  ' +
    #         # #        colored('Scope Id: ', 'yellow') + key['id'])

    def get_app_scope(self):
        """Capture A Specific Application Scope."""
        if (self.args.appscopeid is not None and
                self.args.appscopeshortname is None):
            resp = self.restclient.get('/app_scopes/%s' % self.args.appscopeid)
        if (self.args.appscopeid is None and
                self.args.appscopeshortname is not None):
            self.get_app_scopes()
            if self.app_scope_id is not None:
                resp = self.restclient.get(
                    '/app_scopes/%s' % self.app_scope_id)
            else:
                resp = None
        if (self.args.action != "create_app_scope" and
                self.args.action != "add_user_roles"):
            if resp is not None:
                if resp.status_code == 200:
                    python_data = json.loads(resp.text)
                    print json.dumps(python_data, indent=4)
            else:
                print ("Application Scope Id or Application Scope Short Name "
                       "Does Not Exist!...")

    def get_app_scopes(self):
        """Capture Application Scopes."""
        resp = self.restclient.get('/app_scopes')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if (self.args.action == "create_app" or
                    self.args.action == "create_app_scope" or
                    self.args.action == "get_app_scope" or
                    self.args.action == "add_user_roles"):
                if (self.args.appscopeid is None and
                        self.args.appscopeshortname is not None):
                    for key in python_data:
                        if key['short_name'] == self.args.appscopeshortname:
                            self.app_scope_id = key['id']
                            return
                        else:
                            self.app_scope_id = None
            else:
                if self.args.savetofile:
                    self.save_results(python_data)
                else:
                    print json.dumps(python_data, indent=4)

    def get_flow_dimensions(self):
        """Capture Flow Dimensions."""
        resp = self.restclient.get('/flowsearch/dimensions')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.savetofile:
                self.save_results(python_data)
            else:
                print json.dumps(python_data, indent=4)

    def get_flow_metrics(self):
        """Capture Flow Metrics."""
        resp = self.restclient.get('/flowsearch/metrics')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.savetofile:
                self.save_results(python_data)
            else:
                print json.dumps(python_data, indent=4)

    def get_inventory_dimensions(self):
        """Capture Inventory Dimensions."""
        resp = self.restclient.get('/inventory/search/dimensions')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.savetofile:
                self.save_results(python_data)
            else:
                print json.dumps(python_data, indent=4)

    def get_inventory_filters(self):
        """Capture Inventory Filters."""
        resp = self.restclient.get('/filters/inventories')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.appscopeid is not None:
                data = []
                for key in python_data:
                    if key['app_scope_id'] == self.args.appscopeid:
                        data.append(key)
                print json.dumps(data, indent=4)
            else:
                if self.args.savetofile:
                    self.save_results(python_data)
                else:
                    print json.dumps(python_data, indent=4)

    def get_sensor(self):
        """Get A Sensor."""
        self.get_sensors()

    def get_sensors(self):
        """Capture Sensors."""
        resp = self.restclient.get('/sensors')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.action == "delete_sensor":
                _ips = []
                _uuids = []
                self._sensor_info = {}
                for key in python_data['results']:
                    if key['host_name'] == self.args.hostname:
                        if "deleted_at" in key:
                            print "%s already deleted" % self.args.hostname
                        else:
                            self._sensor_info['host_name'] = key['host_name']
                            for _int in key['interfaces']:
                                if (_int['family_type'] == "IPV4" and
                                        _int['ip'] != "127.0.0.1"):
                                    if _int['ip'] not in _ips:
                                        _ips.append(_int['ip'])
                            if key['uuid'] not in _uuids:
                                _uuids.append(key['uuid'])
                self._sensor_info.update({"ips": _ips})
                self._sensor_info.update({"uuids": _uuids})
                return
            if self.args.action == "get_sensor":
                for key in python_data['results']:
                    if key['host_name'] == self.args.hostname:
                        print json.dumps(key, indent=4)
                return
            else:
                if self.args.savetofile:
                    self.save_results(python_data)
                else:
                    print json.dumps(python_data, indent=4)

    def get_switches(self):
        """Capture Switches."""
        resp = self.restclient.get('/switches')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.savetofile:
                self.save_results(python_data)
            else:
                print json.dumps(python_data, indent=4)

    def get_user(self):
        """Capture Users."""
        resp = self.restclient.get('/users')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            for key in python_data:
                if (key['first_name'] == self.args.userfirstname and
                        key['last_name'] == self.args.userlastname and
                        key['email'] == self.args.useremail.lower()):
                    self.user_id = key['id']
                    self.user_role_ids = key['role_ids']
                    if self.args.action != "get_user":
                        return
                    else:
                        print key['id']
                else:
                    self.user_id = None
                    self.user_role_ids = []

    def get_user_roles(self):
        """Capture User Roles."""
        resp = self.restclient.get('/roles')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.action == "add_user_roles":
                self.roles = []
                for key in python_data:
                    self.roles.append(key['name'])
                return
            if self.args.action == "get_user_roles":
                if self.args.savetofile:
                    self.save_results(python_data)
                else:
                    print json.dumps(python_data, indent=4)
            else:
                for key in python_data:
                    if self.args.userrole is None:
                        print key['id']
                    else:
                        if key['name'] == self.args.userrole:
                            self.user_role_id = key['id']
                            return
                        else:
                            self.user_role_id = None

    def get_users(self):
        """Capture Users."""
        resp = self.restclient.get('/users')
        if resp.status_code == 200:
            python_data = json.loads(resp.text)
            if self.args.savetofile:
                self.save_results(python_data)
            else:
                print json.dumps(python_data, indent=4)

    def read_cli_args(self):
        """
        Read variables from CLI.

        Read CLI variables passed on CLI.
        """

        parser = argparse.ArgumentParser(description='Tetration Commands...')
        parser.add_argument(
            'action', help='Define action to take',
            choices=['add_user_roles', 'add_users', 'add_user_to_role',
                     'create_app', 'create_app_scope', 'delete_app',
                     'delete_sensor', 'delete_users', 'get_app',
                     'get_app_clusters', 'get_apps', 'get_app_scope',
                     'get_app_scopes', 'get_flow_dimensions',
                     'get_flow_metrics', 'get_inventory_dimensions',
                     'get_inventory_filters', 'get_switches', 'get_user_roles',
                     'get_sensor', 'get_sensors', 'get_user', 'get_users',
                     'remove_user_from_role'])
        parser.add_argument(
            '--apiendpoint', help='Tetration API Endpoint', required=False,
            default='https://172.16.5.4')
        parser.add_argument(
            '--apikey', help='Tetration API Key', required=False)
        parser.add_argument(
            '--apisecret', help='Tetration API Secret', required=False)
        parser.add_argument(
            '--appdescription', help='Application Description', required=False)
        parser.add_argument(
            '--appname', help='Application Name', required=False)
        parser.add_argument(
            '--appid', help='Application Id', required=False)
        parser.add_argument(
            '--appscopeid', help='Application Scope Id', required=False)
        parser.add_argument(
            '--appscopeshortname', help='Application Scope Short Name',
            required=False)
        parser.add_argument(
            '--appscopeprimary', help='Application Scope Primary(True|False)',
            required=False, default=False)
        parser.add_argument(
            '--credsfile', help='Path To Credentials file', required=False,
            default="~\\downloads\\api_credentials.json")
        parser.add_argument(
            '--hostname', help='Sensor host name'
        )
        parser.add_argument(
            '--ip', help='IP address', required=False
        )
        parser.add_argument('--readcsv', help='Read input from CSV')
        parser.add_argument(
            '--savetofile', help='Define file to save results to')
        parser.add_argument(
            '--useremail', help='User email', required=False)
        parser.add_argument(
            '--userfirstname', help='User first name', required=False)
        parser.add_argument(
            '--userlastname', help='User last name', required=False)
        parser.add_argument(
            '--userrole', help='Role name to add user to', required=False)
        parser.add_argument(
            '--userroledescription', help='Role name description',
            required=False
        )
        parser.add_argument(
            '--vrf', help='VRF Name', required=False
        )

        self.args = parser.parse_args()
        # if self.args.action == "add_user_to_role":

        if self.args.action == "add_users":
            if self.args.readcsv is None:
                if (self.args.userfirstname is None or
                        self.args.userlastname is None or
                        self.args.useremail is None):
                    parser.error(
                        '--userfirstname and --userlastname and '
                        '--useremail ARE REQUIRED!')
        if self.args.action == "delete_sensor":
            if (self.args.hostname is None or
                    self.args.ip is None):
                parser.error('--hostname and --ip are REQUIRED!')
        if self.args.action == "delete_users":
            if self.args.readcsv is None:
                if (self.args.userfirstname is None or
                        self.args.userlastname is None or
                        self.args.useremail is None):
                    parser.error(
                        '--userfirstname and --userlastname and '
                        '--useremail ARE REQUIRED!')
        if self.args.action == "create_app":
            if self.args.appname is None:
                parser.error('--appname is REQUIRED!')
            if self.args.appscopeid is None:
                if self.args.appscopeshortname is None:
                    parser.error('--appscopeid or --appscopename is REQUIRED!')
            if self.args.appscopeshortname is None:
                if self.args.appscopeid is None:
                    parser.error(
                        '--appscopeid or --appscopeshortname is REQUIRED!')
        if self.args.action == "delete_app":
            if self.args.appid is None:
                parser.error('--appid is REQUIRED!')
        if self.args.action == "get_app":
            if self.args.appname is None and self.args.appid is None:
                parser.error('--appname or --appid are REQUIRED!')
            if (self.args.appname is not None and
                    self.args.appid is None and self.args.appscopeid is None):
                parser.error('--appscopeid is REQUIRED when using --appname!')
        if self.args.action == "get_app_clusters":
            if self.args.appid is None:
                parser.error('--appid is REQUIRED!')
        if self.args.action == "get_app_scope":
            if self.args.appscopeid is None:
                if self.args.appscopeshortname is None:
                    parser.error('--appscopeid or --appscopename is REQUIRED!')
            if self.args.appscopeshortname is None:
                if self.args.appscopeid is None:
                    parser.error(
                        '--appscopeid or --appscopeshortname is REQUIRED!')
        if self.args.action == "get_sensor":
            if self.args.hostname is None:
                parser.error('--hostname is REQUIRED!')
        if self.args.action == "remove_user_from_role":
            if (self.args.userfirstname is None or
                    self.args.userlastname is None or
                    self.args.useremail is None or
                    self.args.userrole is None):
                parser.error(
                    '--userfirstname, --userlastname, --useremail, '
                    'and --userrole ARE REQUIRED!')
        if self.args.credsfile is None:
            if self.args.apikey is None or self.args.apisecret is None:
                parser.error('--apikey and --apisecret ARE REQUIRED!')
        elif self.args.credsfile is not None:
            if self.args.apikey is not None or self.args.apisecret is not None:
                parser.error(
                    '--apikey and --apisecret ARE NOT REQUIRED when '
                    'using --credsfile!')

    def remove_user_from_role(self):
        """Remove A User From A role."""
        # NEED to add ability defined more than one role ####
        self.get_user_roles()
        self.get_user()
        if self.user_role_id is not None:
            if self.user_role_id in self.user_role_ids:
                req_payload = {
                    "role_id": self.user_role_id
                }
                endpoint = '/users/%s/remove_role' % self.user_id
                resp = self.restclient.delete(
                    '%s' % endpoint, json_body=json.dumps(req_payload))
                if resp.status_code == 200:
                    print colored('User successfully remove from role...',
                                  'yellow')
            else:
                print colored('User already removed from role...Skipping',
                              'yellow')
        else:
            print (colored('Role does not exist and user not removed from '
                           'role: ', 'yellow')
                   + self.args.userrole)

    def save_results(self, python_data):
        """Save scan results to file specified in JSON format."""
        with open(self.args.savetofile, 'w') as outfile:
            json.dump(python_data, outfile, sort_keys=True,
                      indent=4, ensure_ascii=False)


if __name__ == '__main__':
    Tetration()
