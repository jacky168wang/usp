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
# File Name: abstract_mtp.py
#
# Description: A generic MTP for receiving and sending USP Messages use by the Proxy
#
"""

class AbstractMtp:
    """A generic MTP for receiving and sending USP Messages use by the Proxy"""
    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve the next incoming message from the Queue"""
        raise NotImplementedError()

    def send_msg(self, payload, to_addr, reply_to_addr):
        """Send the ProtoBuf Serialized Message to the provided address via the Protocol-specific USP Binding"""
        raise NotImplementedError()

    def listen(self):
        """Listen for incoming messages on the Protocol-specific USP Binding"""
        raise NotImplementedError()
