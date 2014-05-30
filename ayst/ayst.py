"""A simple little library for validating whether or not an email
address exists using smtp.

"""
import smtplib
import uuid
from DNS import Base
from DNS.Base import ServerError


# Most of this code taken from emailpie, bioengineered for awesomeness:
# https://github.com/bryanhelmig/emailpie/blob/master/emailpie/utils.py
def dnslookup(name, qtype):
    """Function to return just answer data for any query type"""
    if Base.defaults['server'] == []:
        Base.DiscoverNameServers()

    result = Base.DnsRequest(name=name, qtype=qtype, timout=5).req()
    if result.header['status'] != 'NOERROR':
        raise ServerError("DNS query status: %s" % result.header['status'],
                          result.header['rcode'])
    elif len(result.answers) == 0 and Base.defaults['server_rotate']:
        # check with next DNS server
        result = Base.DnsRequest(name=name, qtype=qtype, timout=5).req()
        if result.header['status'] != 'NOERROR':
            raise ServerError("DNS query status: %s" % result.header['status'],
                              result.header['rcode'])
    return [x['data'] for x in result.answers]

def mxlookup(name):
    """Does an MX lookup of a name. Returns a sorted list of
    (preference, mail exchanger) records

    """
    l = dnslookup(name, qtype='mx')
    l.sort()
    return l

class VerificationException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def smtp_check(user, host, servers):
    """Try to verify that an email address exists via poking
    at SMTP. This often won't work, but is like magic when it
    does. You can verify if it works by giving a random email
    that most certainly shouldn't exist and see if the function
    returns True. If it does, then the server probably doesn't
    allow verification or has wildcards tuned on.

    """
    for server in servers:
        try:
            smtp = smtplib.SMTP()
            smtp.connect(server)
            status, _ = smtp.helo()
            if status != 250:
                smtp.quit()
                continue
            smtp.mail('')
            status, x = smtp.rcpt(user + '@' + host)
            smtp.quit()
            return status == 250
        except smtplib.SMTPException:
            raise VerificationException("Server told you to fuck off.")


class Email:
    def __init__(self, email):
        self._sneaky = None
        self.valid = None
        self.user, self.host = email.split('@')
        self.servers = [server for (_, server) in mxlookup(self.host)]
        if not self.servers:
            raise VerificationException('No MX records for this domain.')
        self.test_user = str(uuid.uuid1())

    def validate(self):
        """Try to validate via smtp that an email address exists.
        If this is the first time validate has been called, tries
        to test a random email to find out if it exists (because
        that often means the server is lying to us. If so, don't
        even bother checking the actual email.

        """
        if self._sneaky is None:
            self._sneaky = smtp_check(self.test_user, self.host, self.servers)
            return self.validate()
        elif self._sneaky is True:
            message = "Server doesn't allow verification or has wildcards " \
                      "enabled."
            raise VerificationException(message)
        else:
            self.valid = smtp_check(self.user, self.host, self.servers)
            return self.valid
