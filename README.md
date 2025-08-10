# CSB-course-project

This project has been created for learning purposes for the course "Cyber Security Base: Project I" (University of Helsinki). The objective is to create a web application with five flaws from the OWASP top 10 -list, and provide fixes for them. The fixes are commented out from the code.

The OWASP top 10 can be found at https://owasp.org/Top10/


## Table of contents
- [Running the application](#running-the-application)
- [FLAW 1: A05:2021–Security Misconfiguration](#flaw-1-a052021security-misconfiguration)
- [FLAW 2: A06:2021–Vulnerable and Outdated Components](#flaw-2-a062021vulnerable-and-outdated-components)
- [FLAW 3: A01:2021–Broken Access Control](#flaw-3-a012021broken-access-control)
- [FLAW 4: A04:2021–Insecure Design](#flaw-4-a042021insecure-design)
- [FLAW 5: A09:2021–Security Logging and Monitoring Failures](#flaw-5-a092021security-logging-and-monitoring-failures)
- [Credits](#credits)


## Running the application

Take the following steps to run the application, but be mindful that the app is not secure in its current state: 

1. Clone the repository to a location of your choice and go to its root directory
2. Create a file .env into the root directory and add a secret key:
```
SECRET_KEY=<your-secret-key>
DEBUG=<bool-value>
``` 
3. Create a virtual environment: $ python3 -m venv venv
4. Activate the virtual environment: $ source venv/bin/activate
5. Install necessary packages using pip: $ pip install -r requirements.txt
6. Run migrations: $ python manage.py migrate
7. Run the application: $ python manage.py runserver
8. Open a browser and navigate to 'http://localhost:8000/'
9. Add new users, login, and send messages


## FLAW 1: A05:2021–Security Misconfiguration

### exact source link pinpointing flaw 1: 
- https://github.com/jokijen/csb-course-project/blob/main/myapp/settings.py#L28
- https://github.com/jokijen/csb-course-project/blob/main/myapp/settings.py#L36
- https://github.com/jokijen/csb-course-project/blob/main/myapp/settings.py#L101

### description of flaw 1: 
There are several security misconfigurations in the settings. The values for ‘SECRET_KEY’ and ‘DEBUG=True’ are hard-coded into the settings.py file that has also been added to a public repository (L28, L34). The secret key relates to cryptographic signing of the application and may allow an attacker to successfully perform an attack. Having ‘DEBUG’ set to ‘True’ allows detailed error messages, which may reveal unnecessary information about the application (e.g. its architecture or database). 

Additionally, all hosts have been allowed by default (L39) instead of only a set list of hosts that the application can serve (i.e. a whitelist). This may make the application susceptible to host header attacks. 

Finally, there are no password validators (L104), so the user would be able to set a very weak password, such as their name or even a single character.

### how to fix it: 
A better way is to add a separate '.env' file that contains the values for ‘SECRET_KEY’ and ‘DEBUG’. This file is then excluded from being added to the repository by adding its name into the '.gitignore' file (L30, L36). If no such file exists, ‘DEBUG’ will evaluate to ‘False’ which is safer.

Additionally, only specified hosts should be allowed (L41), here an empty list. When ‘ALLOWED_HOSTS’ is an empty list and ‘DEBUG’ is ‘True’, Django performs default host validation using the list ['.localhost', '127.0.0.1', '[::1]'] which is suitable for development and testing. 

Finally, there should be proper password validation in place to ensure and encourage a stronger password (L107–120). This means that the user will not be able to set a password that is clearly unsafe and hence easier to guess or brute force. 


## FLAW 2: A06:2021–Vulnerable and Outdated Components

### exact source link pinpointing flaw 2: 
- https://github.com/jokijen/csb-course-project/blob/main/requirements.txt#L9 

### description of flaw 2:
Using packages and libraries with known vulnerabilities makes the application susceptible to attacks. Selenium version 3.141.0 has a known vulnerability that may enable a Cross-Site Request Forgery (CSRF) attack as is noted in the CVE database: 
- https://www.cvedetails.com/version/1429670/Selenium-Selenium-Grid-3.141.0.html

### how to fix it: 
The best practices instruct to always use safe, up-to-date versions of packages and libraries, and actively keep them updated as time moves on. In general, it is important to monitor security advisories as well as published patches and versions. This allows one to stay informed on found vulnerabilities that might affect the security of the application. 

To fix this flaw remove L9 and include the text now commented out on L10, which contains a newer version with no known vulnerabilities that is also compatible with the other packages. Then run ‘pip install -r requirements.txt’ to compete the upgrade. 


## FLAW 3: A01:2021–Broken Access Control

### exact source link pinpointing flaw 3:
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/views.py#L156 

### description of flaw 3:
The user is able to access a conversation that they are not a part of simply by navigating to it by adding the conversation id to the url, for example: localhost:8000/conversation/3/
This is possible due to insufficient authentication of the user trying to access the conversation. In the faulty version there are no checks in place that verify if the user trying to access the conversation is one of the parties of the conversation. This would be a very serious security flaw as it essentially exposes all conversations to any user that is logged in.  

### how to fix it: 
In this case, the flaw may be fixed by adding back commented out lines L158-159. These implement a check: if the user navigating to the conversation is not one of the conversation parties, they are redirected to ‘home’ instead of taken to the conversation. 


## FLAW 4: A04:2021–Insecure Design

### exact source link pinpointing flaw 4:
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/templates/index.html#L20
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/views.py#L55
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/urls.py#L17
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/forms.py#L78

### description of flaw 4:
If a user forgets their password, the credential recovery workflow includes a “questions and answers” option, which is outdated and has been prohibited by the NIST 800-63b, OWASP ASVS, and OWASP Top 10. The reason for this is that other people may also know the answer to the question and this practice is therefore not considered sufficiently secure. 

### how to fix it: 
Instead, a better way of handing credential recovery would be to ask the user to fill in the email they used to register and send them a unique password reset link that is only valid for a limited time period. This is safer, because the user should be the only person who has access to their email, and no password is sent to them. Additionally, it is better to not confirm if the email exists in the database and only give a blanket message when an email is submitted through the form.  

In the app both logics have been implemented to a point (but not the actual resetting, reset link creation and email as it is out of the scope of this course). You can quickly switch over to the more secure implementation by commenting out:
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/templates/index.html#L20
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/forms.py#L6 (L6–35)

… and including:
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/templates/index.html#L21
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/forms.py#L39 (L39–46)

… which will preserve some faulty logic in the background, but remove the question from registration and the credential recovery workflow accessed via the link on the login page. 


## FLAW 5: A09:2021–Security Logging and Monitoring Failures

### exact source link pinpointing flaw 5:
- https://github.com/jokijen/csb-course-project/blob/main/messagesapp/templates/home.html#L5

### description of flaw 5:
Adding unnecessary logging (perhaps for testing purposes) that ends up visible in production makes the application vulnerable to information leakage which may give an attacker valuable information and even enable an attack. In this example, data is revealed through comments left in the home.html file, that reveals field names and values. In this case, the answer to the user’s secret question and information on how it is stored (i.e. as ‘first_name’) are revealed. 

### how to fix it: 
These comments should simply be deleted (L5–10). In general, it is important to ensure that logs and error messages do not contain information that would be valuable to an attacker. Error messages should nonetheless be valuable to the user so they can react appropriately when an error occurs. 


## Credits

- .gitignore template for Python by GitHub (edited by author): https://github.com/github/gitignore/blob/main/Python.gitignore