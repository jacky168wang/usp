# **************************************************************************
# WT-369 USP Message Protocol Buffer Schema
#
#  Copyright (c) 2017, Broadband Forum
#
#  The undersigned members have elected to grant the copyright to
#  their contributed material used in this software:
#    Copyright (c) 2017 ARRIS Enterprises, LLC.
#
# This is draft software, is subject to change, and has not been approved
#  by members of the Broadband Forum. It is made available to non-members
#  for internal study purposes only. For such study purposes, you have the
#  right to make copies and modifications only for distributing this software
#  internally within your organization among those who are working on it
#  (redistribution outside of your organization for other than study purposes
#  of the original or modified works is not permitted). For the avoidance of
#  doubt, no patent rights are conferred by this license.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.
#
# Unless a different date is specified upon issuance of a draft software
#  release, all member and non-member license rights under the draft software
#  release will expire on the earliest to occur of (i) nine months from the
#  date of issuance, (ii) the issuance of another version of the same software
#  release, or (iii) the adoption of the draft software release as final.
#
# BBF software release registry: http:##www.broadband-forum.org/software
# **************************************************************************

"""
#
# File Name: test_utils.py
#
# Description: Unit tests for utils
#
# Functionality: Test the GenericReceivingQueue Class
#
"""

import time

import unittest.mock as mock

from mtp_proxy import utils


def get_mac_uname_results():
    return "Darwin lasts-mbp.lan 16.7.0 Darwin Kernel Version 16.7.0: Mon Nov 13 21:56:25 PST 2017; root:xnu-3789.72.11~1/RELEASE_X86_64 x86_64"

def get_rpi_uname_results():
    return "Linux rpi-controller 4.9.64-v7+ #1053 SMP Tue Nov 21 14:56:27 GMT 2017 armv7l GNU/Linux"

def get_mac_ifconfig_results():
    ifconfig_results = """
    en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
            ether 98:5a:eb:8b:cb:e8
            inet6 fe80::804:8e65:bd04:5bb7%en0 prefixlen 64 secured scopeid 0x4
            inet 99.100.101.102 netmask 0xffffff00 broadcast 192.168.86.255
            nd6 options=201<PERFORMNUD,DAD>
            media: autoselect
            status: active
    """
    return ifconfig_results

def get_rpi_ip_addr_results():
    ip_addr_results = """
    3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
        link/ether b8:27:eb:34:f7:e0 brd ff:ff:ff:ff:ff:ff
        inet 99.100.101.102/24 brd 192.168.86.255 scope global wlan0
           valid_lft forever preferred_lft forever
        inet6 fe80::5f85:8005:2f1a:6ecc/64 scope link
           valid_lft forever preferred_lft forever
    """
    return ip_addr_results


def test_empty_pop():
    queue = utils.GenericReceivingQueue()
    queue_item = queue.pop()

    assert queue_item is None


def test_one_entry():
    payload = "TEST"
    reply_to_addr = "ADDR"
    queue = utils.GenericReceivingQueue()
    queue_item = utils.ExpiringQueueItem(payload, reply_to_addr)
    queue.push(queue_item)
    queue_item = queue.pop()

    assert payload == queue_item.get_payload()
    assert reply_to_addr == queue_item.get_reply_to_addr()


def test_multiple_entries_seq():
    payload1 = "TEST1"
    reply_to_addr1 = "ADDR1"
    payload2 = "TEST2"
    reply_to_addr2 = "ADDR2"
    payload3 = "TEST3"
    reply_to_addr3 = "ADDR3"
    payload4 = "TEST4"
    reply_to_addr4 = "ADDR4"
    queue = utils.GenericReceivingQueue()
    queue_item1 = utils.ExpiringQueueItem(payload1, reply_to_addr1)
    queue_item2 = utils.ExpiringQueueItem(payload2, reply_to_addr2)
    queue_item3 = utils.ExpiringQueueItem(payload3, reply_to_addr3)
    queue_item4 = utils.ExpiringQueueItem(payload4, reply_to_addr4)
    queue.push(queue_item1)
    queue.push(queue_item2)
    queue.push(queue_item3)
    queue.push(queue_item4)
    queue_item1 = queue.pop()
    queue_item2 = queue.pop()
    queue_item3 = queue.pop()
    queue_item4 = queue.pop()

    assert payload1 == queue_item1.get_payload()
    assert reply_to_addr1 == queue_item1.get_reply_to_addr()
    assert payload2 == queue_item2.get_payload()
    assert reply_to_addr2 == queue_item2.get_reply_to_addr()
    assert payload3 == queue_item3.get_payload()
    assert reply_to_addr3 == queue_item3.get_reply_to_addr()
    assert payload4 == queue_item4.get_payload()
    assert reply_to_addr4 == queue_item4.get_reply_to_addr()


def test_multiple_entries_not_seq():
    payload1 = "TEST1"
    reply_to_addr1 = "ADDR1"
    payload2 = "TEST2"
    reply_to_addr2 = "ADDR2"
    payload3 = "TEST3"
    reply_to_addr3 = "ADDR3"
    payload4 = "TEST4"
    reply_to_addr4 = "ADDR4"
    queue = utils.GenericReceivingQueue()
    queue_item1 = utils.ExpiringQueueItem(payload1, reply_to_addr1)
    queue_item2 = utils.ExpiringQueueItem(payload2, reply_to_addr2)
    queue_item3 = utils.ExpiringQueueItem(payload3, reply_to_addr3)
    queue_item4 = utils.ExpiringQueueItem(payload4, reply_to_addr4)
    queue.push(queue_item1)
    queue.push(queue_item2)
    queue_item1 = queue.pop()
    queue.push(queue_item3)
    queue_item2 = queue.pop()
    queue_item3 = queue.pop()
    queue.push(queue_item4)
    queue_item4 = queue.pop()

    assert payload1 == queue_item1.get_payload()
    assert reply_to_addr1 == queue_item1.get_reply_to_addr()
    assert payload2 == queue_item2.get_payload()
    assert reply_to_addr2 == queue_item2.get_reply_to_addr()
    assert payload3 == queue_item3.get_payload()
    assert reply_to_addr3 == queue_item3.get_reply_to_addr()
    assert payload4 == queue_item4.get_payload()
    assert reply_to_addr4 == queue_item4.get_reply_to_addr()


def test_get_msg_found():
    timeout = 15
    payload = "TEST"
    reply_to_addr = "ADDR"
    time_mock = mock.Mock()
    time_mock.return_value = None

    queue = utils.GenericReceivingQueue(5)
    queue_item = utils.ExpiringQueueItem(payload, reply_to_addr)
    queue.push(queue_item)

    with mock.patch("time.sleep", time_mock):
        queue_item = queue.get_msg(timeout)

    assert payload == queue_item.get_payload()
    assert reply_to_addr == queue_item.get_reply_to_addr()


def test_get_msg_not_found_empty_queue():
    timeout = 15
    time_mock = mock.Mock()
    time_mock.return_value = None

    queue = utils.GenericReceivingQueue(5)

    with mock.patch("time.sleep", time_mock):
        queue_item = queue.get_msg(timeout)

    assert queue_item is None


def test_get_msg_no_timeout():
    payload = "TEST"
    reply_to_addr = "ADDR"

    queue = utils.GenericReceivingQueue()
    queue_item = utils.ExpiringQueueItem(payload, reply_to_addr)
    queue.push(queue_item)

    queue_item = queue.get_msg()

    assert payload == queue_item.get_payload()
    assert reply_to_addr == queue_item.get_reply_to_addr()


def test_get_msg_expired():
    timeout = 15
    payload = "TEST"
    time_mock = mock.Mock()
    time_mock.return_value = None
    time_time_mock = mock.Mock()
    time_time_mock.return_value = time.time() + 61

    queue = utils.GenericReceivingQueue(5)
    queue_item = utils.ExpiringQueueItem(payload)
    queue.push(queue_item)

    with mock.patch("time.sleep", time_mock):
        with mock.patch("time.time", time_time_mock):
            queue_item = queue.get_msg(timeout)

    assert queue_item is None


def test_ipaddr_mac_no_intf():
    expected_ip_addr = "99.100.101.102"
    uname_results_mock = mock.Mock()
    ifconfig_results_mock = mock.Mock()

    uname_attrs = {'communicate.return_value': [get_mac_uname_results().encode("utf-8")]}
    uname_results_mock.configure_mock(**uname_attrs)

    ifconfig_results_attrs = {'communicate.return_value': [get_mac_ifconfig_results().encode("utf-8")]}
    ifconfig_results_mock.configure_mock(**ifconfig_results_attrs)

    popen_mock = mock.Mock(side_effect=[uname_results_mock, ifconfig_results_mock])

    ip = utils.IPAddr()

    with mock.patch("subprocess.Popen", popen_mock):
        ipaddr = ip.get_ip_addr()

    assert ipaddr == expected_ip_addr


def test_ipaddr_mac_intf():
    intf = "en0"
    expected_ip_addr = "99.100.101.102"
    uname_results_mock = mock.Mock()
    ifconfig_results_mock = mock.Mock()

    uname_attrs = {'communicate.return_value': [get_mac_uname_results().encode("utf-8")]}
    uname_results_mock.configure_mock(**uname_attrs)

    ifconfig_results_attrs = {'communicate.return_value': [get_mac_ifconfig_results().encode("utf-8")]}
    ifconfig_results_mock.configure_mock(**ifconfig_results_attrs)

    popen_mock = mock.Mock(side_effect=[uname_results_mock, ifconfig_results_mock])

    ip = utils.IPAddr()

    with mock.patch("subprocess.Popen", popen_mock):
        ipaddr = ip.get_ip_addr(intf)

    assert ipaddr == expected_ip_addr


def test_ipaddr_rpi_no_intf():
    expected_ip_addr = "99.100.101.102"
    uname_results_mock = mock.Mock()
    ip_addr_show_results_mock = mock.Mock()

    uname_attrs = {'communicate.return_value': [get_rpi_uname_results().encode("utf-8")]}
    uname_results_mock.configure_mock(**uname_attrs)

    ip_addr_show_attrs = {'communicate.return_value': [get_rpi_ip_addr_results().encode("utf-8")]}
    ip_addr_show_results_mock.configure_mock(**ip_addr_show_attrs)

    popen_mock = mock.Mock(side_effect=[uname_results_mock, ip_addr_show_results_mock])

    ip = utils.IPAddr()

    with mock.patch("subprocess.Popen", popen_mock):
        ipaddr = ip.get_ip_addr()

    assert ipaddr == expected_ip_addr
    

def test_ipaddr_rpi_intf():
    intf = "wlan0"
    expected_ip_addr = "99.100.101.102"
    uname_results_mock = mock.Mock()
    ip_addr_show_results_mock = mock.Mock()

    uname_attrs = {'communicate.return_value': [get_rpi_uname_results().encode("utf-8")]}
    uname_results_mock.configure_mock(**uname_attrs)

    ip_addr_show_attrs = {'communicate.return_value': [get_rpi_ip_addr_results().encode("utf-8")]}
    ip_addr_show_results_mock.configure_mock(**ip_addr_show_attrs)

    popen_mock = mock.Mock(side_effect=[uname_results_mock, ip_addr_show_results_mock])

    ip = utils.IPAddr()

    with mock.patch("subprocess.Popen", popen_mock):
        ipaddr = ip.get_ip_addr(intf)

    assert ipaddr == expected_ip_addr
