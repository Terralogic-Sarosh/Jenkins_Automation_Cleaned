import jenkins
jenkins_server = jenkins.Jenkins("http://localhost:8080/", username='admin', password='6f0538b3fb304d918a5c7d2675221c66')
job_info = jenkins_server.get_job_info('build_test')
print(job_info)
builds = job_info['builds']
print(len(builds))