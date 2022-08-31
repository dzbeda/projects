# Example 1 
### Requirement : 
  1. Break the input domain-name ; Split by .
  2. Add the name partten to a defined string
### Code
domin_name: dudu.zbeda.com   # Defined input. Can be define on external file
{% set domain_pattern = domin_name.split('.') %}  # Define new list names domain_pattern. Each entery is defined based on . split
domain.pattern=(resource\\.{{ domain_pattern|join('\\\\.') }})$ 

### Output: 
domain.pattern=(resource\\.dudu\\.zbeda\\.com)$
