#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example fetches the set of valid ProductBiddingCategories.

Tags: ConstantDataService.getProductBiddingCategoryData
"""

__author__ = 'api.msaniscalchi@gmail.com (Mark Saniscalchi)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


def main(client):
  selector = {
      'predicates': [
          {
              'field': 'Country',
              'operator': 'IN',
              'values': ['US']
          }
      ]
  }

  service = client.GetConstantDataService(version='v201402')
  result = service.GetProductBiddingCategoryData(selector)

  bidding_categories = {}
  root_categories = []

  for product_bidding_category in result:
    id = product_bidding_category['dimensionValue']['value']
    parent_id = None
    name = product_bidding_category['displayValue'][0]['value']

    # Note: There may be cases where there isn't a value.
    if ('parentDimensionValue' in product_bidding_category and
        'value' in product_bidding_category['parentDimensionValue']):
      parent_id = product_bidding_category['parentDimensionValue']['value']

    if id not in bidding_categories:
      bidding_categories[id] = {}

    category = bidding_categories[id]

    if parent_id is not None:
      if parent_id not in bidding_categories:
        bidding_categories[parent_id] = {}

      parent = bidding_categories[parent_id]

      if 'children' not in parent:
        parent['children'] = []

      parent['children'].append(category)
    else:
      root_categories.append(category)

    category['id'] = id
    category['name'] = name

  DisplayCategories(root_categories)


def DisplayCategories(categories, prefix=''):
  for category in categories:
    print '%s%s [%s]' % (prefix, category['name'], category['id'])

    if 'children' in category:
      DisplayCategories(category['children'], '%s%s > ' % (prefix,
                                                           category['name']))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client)