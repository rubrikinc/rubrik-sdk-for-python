import rubrik

rubrik = rubrik.Connect()

vm_name = 'python-sdk-demo'
end_user_name = "pythonsdk"

authorize = rubrik.end_user_authorization(vm_name, end_user_name)
