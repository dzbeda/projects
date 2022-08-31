# Example 1 
## This example breaks the domain name input and add prints it as s strinf
external_fqdn: dudu.zbeda.com   # Defined input. Can be define on external file
{% set domain_pattern = external_fqdn.split('.') %}  # Define new list names domain_pattern. Each entery is defined based on . split
domain.pattern=(resource\\.{{ domain_pattern|join('\\\\.') }})$ 

### Output: domain.pattern=(resource\\.dudu\\.zbeda\\.com)$
