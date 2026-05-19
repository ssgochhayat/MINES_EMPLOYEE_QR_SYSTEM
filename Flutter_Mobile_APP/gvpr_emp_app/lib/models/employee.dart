class Employee {
  final int id;
  final String employeeId;
  final String name;
  final String department;
  final String designation;
  final String mobile;
  final String qrCode;
  final String photo;
  final String joiningLetter;
  final String appointmentLetter;

  Employee({
    required this.id,
    required this.employeeId,
    required this.name,
    required this.department,
    required this.designation,
    required this.mobile,
    required this.qrCode,
    required this.photo,
    required this.joiningLetter,
    required this.appointmentLetter,
  });

  factory Employee.fromJson(Map<String, dynamic> json) {
    return Employee(
      id: json['id'],
      employeeId: json['employee_id'],
      name: json['name'],
      department: json['department'],
      designation: json['designation'],
      mobile: json['mobile'],
      qrCode: json['qr_code'],
      photo: json['photo'],
      joiningLetter: json['joining_letter'],
      appointmentLetter: json['appointment_letter'],
    );
  }
}
