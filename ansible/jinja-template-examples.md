# Example 1 
### Requirement : 
  1. Break the input domain-name ; Split by .
  2. Add the name partten to a defined string
### Code
domin_name: dudu.zbeda.com   #  Defined input. Can be defined on an external file

{% set domain_pattern = domin_name.split('.') %}  # Define a list, named domain_pattern. Each entry is split by .

domain.pattern=(resource\\.{{ domain_pattern|join('\\\\.') }})$ 

### Output: 
domain.pattern=(resource\\.dudu\\.zbeda\\.com)$
