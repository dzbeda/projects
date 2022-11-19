# Description #

## What is OpenSearch ##

OpenSearch is free DB based on Elastic 7 release that requires license
OpenSearch is distributed, community-driven, Apache 2.0-licensed, 100% open-source search and analytics suite used for a broad set of use cases 
like real-time application monitoring, log analytics, and website search. OpenSearch provides a highly scalable system for providing fast access and response 
to large volumes of data with an integrated visualization tool, OpenSearch Dashboards, that makes it easy for users to explore their data. 
OpenSearch is powered by the Apache Lucene search library, and it supports a number of search and analytics capabilities such as k-nearest neighbors (KNN) search, 
SQL, Anomaly Detection, Machine Learning Commons, Trace Analytics, full-text search, and more.

## What is ISM ##

ISM is the life cycle management feature of OpenSearch DB.
Using ISM you can move indices between different states and perform an action on each state.
ISM can be used for moving indices between HOT storage (IOPS intensive) to cold storage (low IOPS) or deleting indices based on time.

    
# How to use this project # 

In input-file.yml file should hodl all indexes list. Each index should be defined with 3 parameter 


1. index_name parameters 
    1. defines the policy name 
    2. The index pattern is defined by this name.  for example, in case of the "audit" index name, the index pattern will be set to audit-* , which will force all indexes starting with the prefix audit to be managed by the ISM policy.
2. min_index_age_in_days parameters 
    1. This defines how long to save an index before deleting it.
    2. Please note that the value describes days
3.status parameters 
    1. disable - if a policy name exists the policy will be deleted. this way you can have default list of index with where status is set to "disable" and for each project you can enable only the relevant indexes
    2. enable - Policy will be created or updated 

 ** Important note **

New policy can manage only indexs that were created after the policy was created. Meaning that indexes that were created before the policy will not be managed by the ISM policy.  Therfore , if you need to update a policy do not delete it and create a new one - just update the policy (this is supported by the ISM installation)


