import jenkins
import time

server = jenkins.Jenkins('http://localhost:8080', username='admin', password='6f0538b3fb304d918a5c7d2675221c66')
jobs = server.get_all_jobs(folder_depth=None)
print(jobs)
for job in jobs:
    print(job['fullname'])
all_jobs_name = []

info = server.get_job_info('Hello_World')

# Loop over builds
print('FifthProject job info : ', server.get_job_info('Hello_World'))
builds = info['builds']
print("builds",builds)
for build in builds:
    print(server.get_build_info('Hello_World', build['number']))
    build_info = server.get_build_info('Hello_World', build['number'])
    print(build_info['result'])

print("##############################################################################")
j_name = 'Hello_World'
server.build_job(j_name)
while True:
    print('Running....')
    if server.get_job_info(j_name)['lastCompletedBuild']['number'] == server.get_job_info(j_name)['lastBuild']['number']:
        print("Last ID %s, Current ID %s"  % (server.get_job_info(j_name)['lastCompletedBuild']['number'], server.get_job_info(j_name)['lastBuild']['number']))
        break
time.sleep(3)
print('Stop....')

build_result = {'FourthProject': {'time': '11:10:2019 15:45:34', 'build_no': 59, 'result': 'SUCCESS'}, 'FifthProject': {'time': '11:10:2019 15:45:34', 'build_no': 63, 'result': 'SUCCESS'}, 'SecondProject': {'time': '11:10:2019 15:45:35', 'build_no': 59, 'result': 'SUCCESS'}, 'Hello_World': {'time': '11:10:2019 15:45:37', 'build_no': 80, 'result': 'FAILURE'}, 'seven_project': {'time': '11:10:2019 15:45:37', 'build_no': 59, 'result': 'SUCCESS'}, 'Six-Project': {'time': '11:10:2019 15:45:40', 'build_no': 59, 'result': 'SUCCESS'}, 'ThirdProject': {'time': '11:10:2019 15:45:40', 'build_no': 59, 'result': 'SUCCESS'}}
