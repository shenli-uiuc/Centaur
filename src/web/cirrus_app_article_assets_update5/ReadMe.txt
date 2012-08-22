Read the following before using the files within this archive.

1. This archive contains source files that belong to the Cirrus VideoPhone sample application posted on the Adobe Flash Player Developer Center: http://www.adobe.com/devnet/flashplayer/articles/rtmfp_cirrus_app.html


* Use these files with the article to build the sample VideoPhone application.


2. Instructions on building VideoPhone sample application for Flash Player 10

This package includes the following files:

VideoPhoneLabs.mxml  - Source file, must be copied to VideoPhoneLabs/src folder 
AbstractIdManager.as - Source file, must be copied to VideoPhoneLabs/src folder 
HttpIdManager.as - Source file, must be copied to VideoPhoneLabs/src folder 
IdManagerError.as - Source file, must be copied to VideoPhoneLabs/src folder 
IdManagerEvent.as - Source file, must be copied to VideoPhoneLabs/src folder 

ReadMe.txt - This file

reg.cgi - Python web script that you need to run at your web server

1. Install Flash Builder 4
2. Please make sure that you have Flash Player 10 debug version installed (http://www.adobe.com/support/flashplayer/downloads.html)
3. Create a new Flex Project called VideoPhoneLabs
4. Copy source files VideoPhoneLabs.mxml (replace existing VideoPhoneLabs.mxml in src folder), AbstractIdManager.as, HttpIdManager.as, IdManagerError.as and IdManagerEvent.as to VideoPhoneLabs/src
5. Specify your developer key in DeveloperKey constant in VideoPhoneLabs.mxml
6. Specify the URL of your web service in WebServiceUrl constant in VideoPhoneLabs.mxml

After these steps, you should be able to build VideoPhoneLabs.

3. Instructions on setting up your web service required for VideoPhone sample application

In order to use the sample application that you built, you need to setup your web server and host the provided Python script (reg.cgi) for exchanging peer IDs. Please note that setting up the web service is not needed for the hosted VideoPhone sample. In VideoPhoneLabs.mxml, please set WebServiceUrl accordingly. You may also use Google Apps to host this web service (minimal modifications required).

The Python script should be placed in the cgi-bin location according to your web server installation.  The database is an SQLite3 database.  In reg.cgi, please edit the location of the database in variable dbFile.  

You also need to create a database scheme using the followings:

CREATE TABLE registrations (
    m_username VARCHAR COLLATE NOCASE,
    m_identity VARCHAR,
    m_updatetime DATETIME,
    
    PRIMARY KEY (m_username)
);

CREATE INDEX registrations_updatetime ON registrations (m_updatetime ASC);

