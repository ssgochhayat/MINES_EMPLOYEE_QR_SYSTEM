import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class EmployeeDetailScreen extends StatelessWidget {
  final Map<String, dynamic> employee;

  const EmployeeDetailScreen({
    super.key,
    required this.employee,
  });

  String value(String key) {
    final raw = employee[key];
    if (raw == null) return '';
    return raw.toString().trim();
  }

  List<Map<String, dynamic>> get documents {
    final rawDocs = employee['documents'];
    if (rawDocs is List) {
      return rawDocs
          .whereType<Map>()
          .map((doc) => Map<String, dynamic>.from(doc))
          .toList();
    }
    return const [];
  }

  @override
  Widget build(BuildContext context) {
    final photo = value('photo');
    final qrCode = value('qr_code');

    return Scaffold(
      backgroundColor: const Color(0xffF1F5F9),
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xff0F172A),
        elevation: 0,
        title: Text(
          value('name').isEmpty ? 'Employee Details' : value('name'),
          style: const TextStyle(fontWeight: FontWeight.w700),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _profileCard(photo, qrCode),
          const SizedBox(height: 16),
          _section(
            title: 'Basic Details',
            icon: Icons.badge_outlined,
            children: [
              _info('Employee ID', value('employee_id')),
              _info('Name', value('name')),
              _info('Gender', value('gender')),
              _info('Father/Spouse Name', value('father_spouse_name')),
              _info('Date of Birth', value('dob')),
              _info('Place of Birth', value('place_of_birth')),
              _info('Nationality', value('nationality')),
              _info('Education Level', value('education_level')),
            ],
          ),
          _section(
            title: 'Employment Details',
            icon: Icons.engineering_outlined,
            children: [
              _info('Joining Date', value('joining_date')),
              _info('Department', value('department')),
              _info('Designation', value('designation')),
              _info('Category', value('category')),
              _info('Employment Type', value('employment_type')),
              _info('Posting Details', value('posting_details')),
              _info('Pay', value('pay')),
              _info('Promotion', value('promotion')),
              _info('Service Book No', value('service_book_no')),
            ],
          ),
          _section(
            title: 'Government Details',
            icon: Icons.account_balance_outlined,
            children: [
              _info('UAN', value('uan')),
              _info('PAN', value('pan')),
              _info('AADHAAR', value('aadhaar')),
              _info('ESIC IP', value('esic_ip')),
              _info('EPS/NPS', value('eps_nps')),
              _info('Family Details', value('family_details')),
            ],
          ),
          _section(
            title: 'Contact & Bank',
            icon: Icons.contact_phone_outlined,
            children: [
              _info('Mobile', value('mobile')),
              _info('Bank Account No', value('bank_account_no')),
              _info('Bank Name', value('bank_name')),
              _info('IFSC', value('ifsc')),
              _info('Present Address', value('present_address')),
              _info('Permanent Address', value('permanent_address')),
            ],
          ),
          _section(
            title: 'Nominee & Exit',
            icon: Icons.assignment_ind_outlined,
            children: [
              _info('Nominee Name', value('nominee_name')),
              _info('Exit Date', value('exit_date')),
              _info('Exit Reason', value('exit_reason')),
              _info('Identification Mark', value('identification_mark')),
              _info('Remarks', value('remarks')),
            ],
          ),
          _documentsSection(),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _profileCard(String photo, String qrCode) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: _cardDecoration(),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            radius: 42,
            backgroundColor: const Color(0xffDBEAFE),
            backgroundImage: photo.isNotEmpty ? NetworkImage(photo) : null,
            child: photo.isEmpty
                ? const Icon(
                    Icons.person,
                    color: Color(0xff2563EB),
                    size: 42,
                  )
                : null,
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  value('name').isEmpty ? 'Unnamed Employee' : value('name'),
                  style: const TextStyle(
                    color: Color(0xff0F172A),
                    fontSize: 21,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  value('designation').isEmpty
                      ? 'Designation not set'
                      : value('designation'),
                  style: const TextStyle(
                    color: Color(0xff64748B),
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    _chip(Icons.apartment, value('department')),
                    _chip(Icons.phone, value('mobile')),
                  ],
                ),
              ],
            ),
          ),
          if (qrCode.isNotEmpty)
            Container(
              width: 70,
              height: 70,
              padding: const EdgeInsets.all(5),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xffE2E8F0)),
              ),
              child: Image.network(qrCode, fit: BoxFit.contain),
            ),
        ],
      ),
    );
  }

  Widget _section({
    required String title,
    required IconData icon,
    required List<Widget> children,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(18),
      decoration: _cardDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: const Color(0xff2563EB)),
              const SizedBox(width: 10),
              Text(
                title,
                style: const TextStyle(
                  color: Color(0xff0F172A),
                  fontSize: 18,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          ...children,
        ],
      ),
    );
  }

  Widget _documentsSection() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: _cardDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.folder_copy_outlined, color: Color(0xff2563EB)),
              SizedBox(width: 10),
              Text(
                'Documents',
                style: TextStyle(
                  color: Color(0xff0F172A),
                  fontSize: 18,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          _documentButton('Joining Letter', value('joining_letter')),
          _documentButton('Appointment Letter', value('appointment_letter')),
          if (documents.isEmpty &&
              value('joining_letter').isEmpty &&
              value('appointment_letter').isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 14),
              child: Center(
                child: Text(
                  'No documents uploaded',
                  style: TextStyle(color: Color(0xff64748B)),
                ),
              ),
            ),
          ...documents.map((doc) {
            final name = (doc['document_name'] ?? 'Employee Document')
                .toString()
                .trim();
            final url = (doc['file'] ?? '').toString().trim();
            return _documentButton(name.isEmpty ? 'Employee Document' : name, url);
          }),
        ],
      ),
    );
  }

  Widget _documentButton(String title, String url) {
    if (url.isEmpty) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xffF8FAFC),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xffE2E8F0)),
      ),
      child: Row(
        children: [
          const Icon(Icons.description_outlined, color: Color(0xffDC2626)),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
          ),
          TextButton.icon(
            onPressed: () => _openUrl(url),
            icon: const Icon(Icons.open_in_new, size: 18),
            label: const Text('Open'),
          ),
        ],
      ),
    );
  }

  Widget _info(String label, String rawValue) {
    final display = rawValue.isEmpty ? 'Not provided' : rawValue;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 132,
            child: Text(
              label,
              style: const TextStyle(
                color: Color(0xff64748B),
                fontSize: 13,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Expanded(
            child: Text(
              display,
              style: TextStyle(
                color: rawValue.isEmpty
                    ? const Color(0xff94A3B8)
                    : const Color(0xff0F172A),
                fontSize: 14,
                fontWeight: rawValue.isEmpty ? FontWeight.w500 : FontWeight.w700,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _chip(IconData icon, String text) {
    if (text.isEmpty) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
      decoration: BoxDecoration(
        color: const Color(0xffEFF6FF),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 15, color: const Color(0xff2563EB)),
          const SizedBox(width: 6),
          Text(
            text,
            style: const TextStyle(
              color: Color(0xff1D4ED8),
              fontSize: 12,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }

  BoxDecoration _cardDecoration() {
    return BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.04),
          blurRadius: 14,
          offset: const Offset(0, 8),
        ),
      ],
    );
  }

  Future<void> _openUrl(String url) async {
    final uri = Uri.tryParse(url);
    if (uri == null) return;

    await launchUrl(uri, mode: LaunchMode.externalApplication);
  }
}
