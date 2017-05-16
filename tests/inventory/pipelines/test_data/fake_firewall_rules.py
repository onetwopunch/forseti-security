# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test firewall rules data."""


FAKE_FIREWALL_RULES = [
    {'aaaaa': '111'},
    {'bbbbb': '222'}
]

EXPECTED_FIREWALL_RULES_MAP_SHORT = {
    'foo11111': {'aaaaa': '111'},
    'foo22222': {'bbbbb': '222'}
}

EXPECTED_FIREWALL_RULES_MAP =  {
    'foo11111': [
        {
            'allowed': [{'IPProtocol': 'tcp',
                          'ports': ['0-65535']},
                          {'IPProtocol': 'udp',
                          'ports': ['0-65535']},
                         {'IPProtocol': 'icmp'}],
            'creationTimestamp': '2016-11-18T21:24:25.263-08:00',
            'description': 'Allow internal traffic on the default network',
            'id': '2726639735056522470',
            'kind': 'compute#firewall',
            'name': 'default-allow-internal',
            'network': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/networks/default',
            'selfLink': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/firewalls/default-allow-internal',
            'sourceRanges': ['10.128.0.0/9']
        },
        {
            'allowed': [{'IPProtocol': 'tcp'},
                         {'IPProtocol': 'udp'},
                         {'IPProtocol': 'icmp'},
                         {'IPProtocol': 'esp'},
                         {'IPProtocol': 'ah'},
                         {'IPProtocol': 'sctp'}],
            'creationTimestamp': '2016-11-18T21:59:13.812-08:00',
            'description': '',
            'id': '8531581871493108958',
            'kind': 'compute#firewall',
            'name': 'gke-canary-east-67b092c4-all',
            'network': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/networks/default',
            'selfLink': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/firewalls/gke-canary-east-67b092c4-all',
            'sourceRanges': ['10.48.0.0/14']
        }
    ],
    'foo22222': [
        {
            'allowed': [{'IPProtocol': 'icmp'}],
            'creationTimestamp': '2016-11-18T21:24:12.820-08:00',
            'description': 'Allow ICMP from anywhere',
            'id': '1933330271571173139',
            'kind': 'compute#firewall',
            'name': 'default-allow-icmp',
            'network': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/networks/default',
            'selfLink': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/firewalls/default-allow-icmp',
            'sourceRanges': ['0.0.0.0/0']
        },
        {
            'allowed': [{'IPProtocol': 'tcp',
                          'ports': ['0-65535']},
                         {'IPProtocol': 'udp',
                          'ports': ['0-65535']},
                         {'IPProtocol': 'icmp'}],
            'creationTimestamp': '2016-11-18T21:24:12.815-08:00',
            'description': 'Allow internal traffic on the default network',
            'id': '5117898408153210643',
            'kind': 'compute#firewall',
            'name': 'default-allow-internal',
            'network': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/networks/default',
            'selfLink': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/firewalls/default-allow-internal',
            'sourceRanges': ['10.128.0.0/9']
        }
    ]
 }


EXPECTED_LOADABLE_FIREWALL_RULES = [
    {
        'firewall_rule_id': '1933330271571173139',
        'firewall_rule_name': 'default-allow-icmp',
        'project_id': 'foo22222',
        'firewall_rule_target_tags': 'null',
        'firewall_rule_create_time': '2016-11-18 21:24:12',
        'firewall_rule_allowed': 'null',
        'firewall_rule_network': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/networks/default',
        'firewall_rule_self_link': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/firewalls/default-allow-icmp',
        'firewall_rule_description': 'Allow ICMP from anywhere',
        'raw_firewall_rule': '{"network": "https://www.googleapis.com/compute/v1/projects/foo22222/global/networks/default", "kind": "compute#firewall", "sourceRanges": ["0.0.0.0/0"], "description": "Allow ICMP from anywhere", "allowed": [{"IPProtocol": "icmp"}], "creationTimestamp": "2016-11-18T21:24:12.820-08:00", "id": "1933330271571173139", "selfLink": "https://www.googleapis.com/compute/v1/projects/foo22222/global/firewalls/default-allow-icmp", "name": "default-allow-icmp"}',
        'firewall_rule_source_ranges': '["0.0.0.0/0"]',
        'firewall_rule_source_tags': 'null',
    },
    {
        'firewall_rule_id': '5117898408153210643',
        'firewall_rule_name': 'default-allow-internal',
        'project_id': 'foo22222',
        'firewall_rule_target_tags': 'null',
        'firewall_rule_create_time': '2016-11-18 21:24:12',
        'firewall_rule_allowed': 'null',
        'firewall_rule_network': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/networks/default',
        'firewall_rule_self_link': 'https://www.googleapis.com/compute/v1/projects/foo22222/global/firewalls/default-allow-internal',
        'firewall_rule_description': 'Allow internal traffic on the default network',
        'raw_firewall_rule': '{"network": "https://www.googleapis.com/compute/v1/projects/foo22222/global/networks/default", "kind": "compute#firewall", "sourceRanges": ["10.128.0.0/9"], "description": "Allow internal traffic on the default network", "allowed": [{"IPProtocol": "tcp", "ports": ["0-65535"]}, {"IPProtocol": "udp", "ports": ["0-65535"]}, {"IPProtocol": "icmp"}], "creationTimestamp": "2016-11-18T21:24:12.815-08:00", "id": "5117898408153210643", "selfLink": "https://www.googleapis.com/compute/v1/projects/foo22222/global/firewalls/default-allow-internal", "name": "default-allow-internal"}',
        'firewall_rule_source_ranges': '["10.128.0.0/9"]',
        'firewall_rule_source_tags': 'null',
    },
    {
        'firewall_rule_id': '2726639735056522470',
        'firewall_rule_name': 'default-allow-internal',
        'project_id': 'foo11111',
        'firewall_rule_target_tags': 'null',
        'firewall_rule_create_time': '2016-11-18 21:24:25',
        'firewall_rule_allowed': 'null',
        'firewall_rule_network': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/networks/default',
        'firewall_rule_self_link': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/firewalls/default-allow-internal',
        'firewall_rule_description': 'Allow internal traffic on the default network',
        'raw_firewall_rule': '{"network": "https://www.googleapis.com/compute/v1/projects/foo11111/global/networks/default", "kind": "compute#firewall", "sourceRanges": ["10.128.0.0/9"], "description": "Allow internal traffic on the default network", "allowed": [{"IPProtocol": "tcp", "ports": ["0-65535"]}, {"IPProtocol": "udp", "ports": ["0-65535"]}, {"IPProtocol": "icmp"}], "creationTimestamp": "2016-11-18T21:24:25.263-08:00", "id": "2726639735056522470", "selfLink": "https://www.googleapis.com/compute/v1/projects/foo11111/global/firewalls/default-allow-internal", "name": "default-allow-internal"}',
        'firewall_rule_source_ranges': '["10.128.0.0/9"]',
        'firewall_rule_source_tags': 'null',
    },
    {
        'firewall_rule_id': '8531581871493108958', 
        'firewall_rule_name': 'gke-canary-east-67b092c4-all',
        'project_id': 'foo11111',
        'firewall_rule_target_tags': 'null',
        'firewall_rule_create_time': '2016-11-18 21:59:13',
        'firewall_rule_allowed': 'null',
        'firewall_rule_network': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/networks/default',
        'firewall_rule_self_link': 'https://www.googleapis.com/compute/v1/projects/foo11111/global/firewalls/gke-canary-east-67b092c4-all',
        'firewall_rule_description': '',
        'raw_firewall_rule': '{"network": "https://www.googleapis.com/compute/v1/projects/foo11111/global/networks/default", "kind": "compute#firewall", "sourceRanges": ["10.48.0.0/14"], "description": "", "allowed": [{"IPProtocol": "tcp"}, {"IPProtocol": "udp"}, {"IPProtocol": "icmp"}, {"IPProtocol": "esp"}, {"IPProtocol": "ah"}, {"IPProtocol": "sctp"}], "creationTimestamp": "2016-11-18T21:59:13.812-08:00", "id": "8531581871493108958", "selfLink": "https://www.googleapis.com/compute/v1/projects/foo11111/global/firewalls/gke-canary-east-67b092c4-all", "name": "gke-canary-east-67b092c4-all"}',
        'firewall_rule_source_ranges': '["10.48.0.0/14"]',
        'firewall_rule_source_tags': 'null',
    }
]
