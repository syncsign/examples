# HTTPS Request Example

This is an example of how to access a web service over https requests.

## How to add a built-in root CA for a domain (example.com)?

- run: ``openssl s_client -showcerts -connect example.com:443 -servername example.com | grep depth``
- Check the first line, e.g.: ``... CN = DigiCert Global Root CA``
- Download the latest file: https://ccadb-public.secure.force.com/mozilla/IncludedCACertificateReportPEMCSV
- Search for ``DigiCert Global Root CA`` in the CSV, and copy the last column's root CA here
