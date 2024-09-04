import json
import sqlite3
import xml.etree.ElementTree as ET

try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

cur = conn.cursor()

def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False

def store_data_as_json(data, filename):
    # convert the data dictionary into a json string
    json_string = json.dumps(data, indent=2)
    # open and write into the json file
    file = open(filename, 'w', encoding='utf-8')
    file.write(json_string)
    file.close()
    
def store_data_as_xml(data, filename):

    # create a root for the data
    root = ET.Element('data')

    for item in data:
        entity = ET.SubElement(root, 'entity')
        for key, value in item.items():
            sub_element = ET.SubElement(entity, key)
            sub_element.text = str(value)
    
    # create a tree based on the root and data
    tree = ET.ElementTree(root)

    # save to file and display xml
    tree.write(filename)
    xml_string = ET.tostring(root, encoding='utf-8').decode()
    print(xml_string)

def offer_to_store(data):
    while True:
        print("\nWould you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("\nSpecify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
            elif ext == 'json':
                store_data_as_json(data, filename)
            else:
                print("\nInvalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

usage = '''
What would you like to do?

d                          - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("\nWelcome to the data querying app!\n")

while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # demo - a nice bit of code from me to you - this prints all student names and surnames :)
        data = cur.execute("SELECT * FROM Student")
        names_list =[]
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
            names_dict = {'firstname': firstname,'surname': surname}
            names_list.append(names_dict)
        print(names_list)

    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1): # user_input: vs CD00100200314
            continue
        student_id = args[0]
        data = cur.execute(
                        '''SELECT * 
                           FROM StudentCourse INNER JOIN Course 
                           ON StudentCourse.course_code = Course.course_code 
                           WHERE StudentCourse.student_id = ? ''', (student_id,))
        
        # Convert data into list of dictionaries to enable json/xml form
        course_name_list = []
        for student_id, course_code, mark, is_complete, _, course_name, course_description, teacher_id, course_level in data:
            print(f"\ncourse_name: {course_name}\n")
            course_name_dict = {'student_id': student_id, 
                                'course_code': course_code, 
                                'mark': mark, 
                                'is_complete': is_complete, 
                                'course_name': course_name, 
                                'course_description': course_description, 
                                'teacher_id': teacher_id, 
                                'course_level': course_level,
                                }
            course_name_list.append(course_name_dict)

        # Store the student course_name data in json/xml form
        offer_to_store(course_name_list)

    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2): # user_input: la Kamala Khan
            continue
        firstname, surname = args[0], args[1]
        data = cur.execute(
                        '''SELECT * 
                           FROM Student INNER JOIN Address 
                           ON Address.address_id = Student.address_id 
                           WHERE Student.first_name = ? AND Student.last_name = ? ''', (firstname, surname))
        
        # Convert data into list of dictionaries to enable json/xml form
        address_list = []
        for student_id, first_name, last_name, email, address_id, _, street, city, province, postal_code, country in data:
            print(f"\nstreet: {street}")
            print(f"city: {city}\n")
            address_dict = {'student_id': student_id, 
                            'first_name': first_name, 
                            'last_name': last_name, 
                            'email': email, 
                            'address_id': address_id, 
                            'street': street, 
                            'city': city, 
                            'province': province, 
                            'postal_code': postal_code, 
                            'country' :country,
                            }
            address_list.append(address_dict)
    
        # Store the student address data in json/xml form
        offer_to_store(address_list)
    
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):# user_input: lr CD00100200314
            continue
        student_id = args[0]
        data = cur.execute(
                        '''SELECT * 
                           FROM Review  
                           WHERE Review.student_id = ? ''', (student_id,))
        
        # Convert data into list of dictionaries to enable json/xml form
        review_list = []
        for review_id, review_text, completeness, efficiency, style, documentation, student_id, course_code in data:
            print(f'\ncompleteness: {completeness}')
            print(f'efficiency: {efficiency}')
            print(f'style: {style}')
            print(f'documentation: {documentation}')
            print(f'review_text: {review_text}\n')
            review_dict = {'review_id': review_id, 
                           'student_id': student_id, 
                           'course_code': course_code, 
                           'completeness': completeness, 
                           'efficiency': efficiency, 
                           'style': style, 
                           'documentation': documentation,  
                           'review_text': review_text, 
                           }
            review_list.append(review_dict)

        # Store the student review data in json/xml
        offer_to_store(review_list)

    elif command == 'lc':# list all courses given by teacher_id
        if usage_is_incorrect(user_input, 1):# user_input: lc MZ004
            continue
        teacher_id = args[0]
        data = cur.execute(
                        '''SELECT * 
                           FROM Course  
                           WHERE Course.teacher_id = ? ''', (teacher_id,))
        # Convert the data into a list of dictionaries to enable conversion
        course_name_list = []
        for course_code, course_name, course_description, teacher_id, course_level in data:
            print(f"\ncourse_name: {course_name}\n")
            course_name_dict = {'course_code': course_code, 
                                'course_name': course_name, 
                                'course_description': course_description, 
                                'teacher_id': teacher_id, 
                                'course_level': course_level, 
                                }
            course_name_list.append(course_name_dict)
    
        # Store the teacher course data in json/xml
        offer_to_store(course_name_list)

    elif command == 'lnc':# list all students who haven't completed their course
        data = cur.execute(
                        '''SELECT * 
                           FROM Student INNER JOIN StudentCourse INNER JOIN Course 
                           ON Student.student_id = StudentCourse.student_id
                           AND StudentCourse.course_code = Course.course_code 
                           WHERE is_complete = ? ''', (0,))
        
        # Convert the data into a list of dictionaries to enable conversion
        incomplete_list = []
        for student_id, first_name, last_name, email, _, _, _, _, is_complete, course_code, course_name, course_description, teacher_id, course_level in data:
            print(f"\nstudent_id: {student_id}")
            print(f"first_name: {first_name}") 
            print(f"last_name: {last_name}")
            print(f"email: {email}")
            print(f"course_name: {course_name}\n")
            incomplete_dict = {'student_id': student_id, 
                               'first_name': first_name, 
                               'last_name': last_name, 
                               'email': email, 
                               'is_complete': is_complete, 
                               'course_code': course_code, 
                               'course_name': course_name, 
                               'course_description': course_description, 
                               'teacher_id': teacher_id, 
                               'course_level': course_level,
                               }
            incomplete_list.append(incomplete_dict)
    
        # Store data for student's who haven't completed in json/xml
        offer_to_store(incomplete_list)
    
    elif command == 'lf':# list all students who have completed their course and got a mark <= 30
        data = cur.execute(
                        '''SELECT * 
                           FROM Student INNER JOIN StudentCourse INNER JOIN Course 
                           ON Student.student_id = StudentCourse.student_id
                           AND StudentCourse.course_code = Course.course_code 
                           WHERE is_complete = ? AND mark <= ? ''', (1, 30))
        
        # Convert the data into a list of dictionaries to enable conversion
        complete_list = []
        for student_id, first_name, last_name, email, _, _, _, mark, is_complete, course_code, course_name, course_description, teacher_id, course_level in data:
            print(f"\nstudent_id: {student_id}")
            print(f"first_name: {first_name}") 
            print(f"last_name: {last_name}")
            print(f"email: {email}")
            print(f"course_name: {course_name}")
            print(f"mark: {mark}\n")
            complete_dict = {'student_id': student_id, 
                               'first_name': first_name, 
                               'last_name': last_name, 
                               'email': email, 
                               'mark': mark, 
                               'is_complete': is_complete, 
                               'course_code': course_code, 
                               'course_name': course_name, 
                               'course_description': course_description, 
                               'teacher_id': teacher_id, 
                               'course_level': course_level,
                               }
            complete_list.append(complete_dict)
        
        # Store data for student's who have completed their course in json/xml
        offer_to_store(complete_list)
    
    elif command == 'e':# list address by name and surname
        print("Programme exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")
    
# References
# 1) https://www.youtube.com/watch?v=daefaLgNkw0
# 2) https://www.youtube.com/watch?v=lZ7kYXImeb0

    