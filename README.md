# ContactBook
Contactbook is an app with main focus on maintaining the contact details of different users.
Admin can create different contacts and can associate any number of contact numbers to a particular user's contact info.

## Contact Book features:
    1. Admin can add contacts to the system with certain constraints:
        a) Each contact can have multiple phone numbers but should have a unique email_address
    2. One can search a contact in the contact book using name or email_address.
    3. Multiple Phone numbers can be added using create/update endpoint.
    4. Partial update of contact's basic info can be done in system.
    5. Any contact can be deleted as well as any phone number of a contact can be deleted.
    6. There is pagination available in get api with info about the total number of records available and next page meta information.
    7. Basic Authentication is used for the purpose of authenticating a user to use the system.

## Follow these steps to execute after cloning:
    ### Create Virtual Environment
    python3 -m venv .venv_contactbook
    
    ### Activate virtualenv
    source .venv_contactbook/bin/activate
        
    ###Install dependencies
    pip install -r requirements.txt
        
    ### Run migrations
    python manage.py migrate
        
    ### To test after any changes
    python manage.py test
        
    ### To run the module on local machine
    python manage.py runserver
