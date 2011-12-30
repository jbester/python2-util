################################################################################
# File     : pub.py
# Function : Publish/Subscribe Library
################################################################################
# Newest version can be obtained at http://www.freshlime.org
# Send comments or questions to code at freshlime dot org
################################################################################
# Copyright (c) 2011, J. Bester
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * The name of the authors names of its contributors may be used to 
#       endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

import collections

__subscribers = collections.defaultdict(list)
__events = []
__inprogress = False


def listen( topic, handler ):
	"""
	Listen to the topic specified
	@param topic: topic to listen for 
	@param handler: method, static method, or function to handle the topic
	@return: None
	"""
	global __subscribers
	print 'listen',topic
	__subscribers[topic].append(handler)

def emit( topic, *args, **kw ):
	"""
	Send a topic
	
	Note: this function preserves global ordering of topics.
	If you emit topic A which in turn emits topic B.  All handlers
	of A will be called prior to any processing of topic B
	@param topic: topic name
	@param *args: ordered arguments
	@param **kw: keyword arguments
	"""
	global __inprogress, __events, __subscribers
	__events.append( (topic, args, kw) )
	# if an event sends an additional event queue it up 
	# this ensures global ordering of topics i.e.
	# if you have an ordered set of three topics A, B, C
	# all of A handlers are processed prior to B being processed
	if __inprogress == False:
		__inprogress = True
		while len(__events) > 0:	
			evt =  __events.pop(0)
			(topic, args, kw) = evt
			for listener in __subscribers[topic]:
				try:
					listener( *args, **kw )	
				except:
					pass	
		__inprogress = False

