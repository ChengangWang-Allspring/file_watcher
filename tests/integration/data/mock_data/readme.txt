preparation check list before starting integration test

1. Ensure local folders exists 
c:\temp\tests\integration\source    
c:\temp\tests\integration\inbound
c:\temp\tests\integration\archive

2. An S3 bucket avaialbe for read and write, for example: "s3-agtps01-use-dev"

s3://s3-agtps01-use-dev/test/integration/source
s3://s3-agtps01-use-dev/test/integration/inbound
s3://s3-agtps01-use-dev/test/integration/archive

3. make sure "insert_intgr_test.sql" is correct reflecting the above local path and s3 URI
run the "insert_intgr_test.sql" in test database table

4. make sure job_name are set up in parametrize list
 in test_integration.py function test_execute_job()

4. run pytest
pytest test_integration.py -v -s
