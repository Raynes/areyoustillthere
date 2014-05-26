"""Heavily impure tests."""
import ayst
import nose
import nose.tools as nt

def test_mxlookup():
    """Test that mxlookup returns preference numbers
    and domains.

    """
    for (pref, server) in ayst.mxlookup('raynes.me'):
        nt.assert_is_instance(pref, int)
        nt.assert_not_equals(server.find('GOOGLE'), -1)


def test_validate():
    """Test that we can validate emails with smtp servers
    that allow it.

    """
    x = ayst.Email('danopia@gmail.com')
    nt.assert_is_none(x.valid)
    nt.assert_true(x.validate())
    nt.assert_true(x.valid)


def test_missing_email():
    """Test that we properly detect emails not existing."""
    x = ayst.Email('thisdoesntexist@scopely.com')
    nt.assert_is_none(x.valid)
    nt.assert_false(x.validate())
    nt.assert_false(x.valid)


@nt.raises(ayst.VerificationException)
def test_bitchy_servers():
    """Test that we can gracefully handle if a server is
    lying to us or doesn't want us around.

    """
    x = ayst.Email('nowaythisexists@riotgames.com')
    x.validate()
