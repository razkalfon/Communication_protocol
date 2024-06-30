# Raz kalfon- 213006083

import sys

global_variable = True

class Packet:
    def _init_(self, source_address, destination_address, sequence_number, is_ack=False, data=None):
        #Initialize a Packet object.
        self.__source_address = source_address
        self.__destination_address = destination_address
        self.__sequence_number = sequence_number
        self.__is_ack = is_ack
        self.__data = data

    def _repr_(self):
        #Return a string representation of the Packet object.
        return f"Packet(Source IP:{self._source_address}, Dest IP: {self.destination_address},#Seq: {self.sequence_number}, Is ACK:{self.is_ack}, Data: {self._data})"

    def get_source_address(self):
        #Get the source address of the packet.
        return self.__source_address

    def get_destination_address(self):
        #Get the destination address of the packet.
        return self.__destination_address

    def get_sequence_number(self):
        #Get the sequence number of the packet.
        return self.__sequence_number

    def set_sequence_number(self, seq_num):
        #Set the sequence number of the packet.
        self.__sequence_number = seq_num

    def get_is_ack(self):
        #Check if the packet is an acknowledgment.
        return self.__is_ack

    def get_data(self):
        #Get the data contained within the packet.
        return self.__data


class Communicator:

    def _init_(self, address):
        #Initialize a Communicator object
        self.__address = address
        self.__current_seq_num = None

    def get_address(self):
        #Get the IP address of the communicator.
        return self.__address

    def get_current_sequence_number(self):
        #Get the current sequence number
        return self.__current_seq_num

    def set_current_sequence_number(self, seq_num):
        #Set the current sequence number
        self.__current_seq_num = seq_num

    def send_packet(self, packet):
        #Send a packet.
        print(f"Sender: Packet Seq Num:{self.get_current_sequence_number()} was sent")
        return packet

    def increment_current_seq_num(self):
        #Increment the current sequence number
        if self.__current_seq_num is not None:
            self.__current_seq_num += 1


class Sender(Communicator):
    def _init_(self, address, num_letters_in_packet):
        #Initialize a Sender object
        super()._init_(address)
        self.__num_letters_in_packet = num_letters_in_packet

    def prepare_packets(self, message, destination_address):
        # Prepare packets for transmission
        packets = []
        num_special_chars = 0
        for char in message:
            if 33 <= ord(char) <= 47 or 58<=ord(char)<=64 or 91<=ord(char)<=96 or 123<=ord(char)<=126: #check if the char is between numbers of asci table
                num_special_chars += 1
        if num_special_chars == len(message): ## compare the number of chars and the size of messages
            if message!="": ## to avoid the empty string  if message=="" i skip it
                print("Only special numbers")
                sys.exit() ## to avoid printing  "Not Sending an Empty String" i exit the programa

        seq_num = self.get_current_sequence_number() if self.get_current_sequence_number() is not None else 0
        for i in range(0, len(message), self.__num_letters_in_packet):
            # Ensure each packet is of fixed length by padding if necessary
            data = message[i:i + self._num_letters_in_packet].ljust(self._num_letters_in_packet)
            packet = Packet(source_address=self.get_address(), destination_address=destination_address,
                            sequence_number=seq_num, data=data)
            packets.append(packet)
            seq_num += 1

        return packets

    def receive_ack(self, acknowledgment_packet):
        #Receive acknowledgment for sent packet
        if acknowledgment_packet.get_is_ack():
            return True
        else:
            return False


class Receiver(Communicator):
    #Class representing a receiver in a communication network.

    def _init_(self, address):
        #Initialize a Receiver object
        super()._init_(address)
        self.__received_packets = []

    def receive_packet(self, packet):
        #Receive a packet
        if packet is None:
            return None

        self.__received_packets.append(packet)
        # Send acknowledgment back to the sender
        acknowledgement = Packet(source_address=packet.get_destination_address(),
                                 destination_address=packet.get_source_address(),
                                 sequence_number=packet.get_sequence_number(),
                                 is_ack=True)
        print(f"Received packet seq num: {packet.get_sequence_number()}")
        return acknowledgement

    def get_message_by_received_packets(self):
        #Retrieve the full message assembled from received packets
        message = ""
        for packet in self.__received_packets:
            message += packet.get_data()
        return message


if _name_ == '_main_':
    source_address = "192.168.1.1"
    destination_address = "192.168.2.2"
    message = "dsfsdfsd#"
    num_letters_in_packet = 6

    sender = Sender(source_address, num_letters_in_packet)
    receiver = Receiver(destination_address)

    packets = sender.prepare_packets(message, receiver.get_address())

    if packets:
        start_interval_index = packets[0].get_sequence_number()
        sender.set_current_sequence_number(start_interval_index)
        receiver.set_current_sequence_number(start_interval_index)

        last_packet_sequence_num = packets[-1].get_sequence_number()
        receiver_current_packet = receiver.get_current_sequence_number()

        while receiver_current_packet <= last_packet_sequence_num:
            current_index = sender.get_current_sequence_number()
            packet = packets[current_index]
            packet = sender.send_packet(packet)

            ack = receiver.receive_packet(packet)

            result = sender.receive_ack(ack)

            if result == True:
                sender.increment_current_seq_num()
                receiver.increment_current_seq_num()

            receiver_current_packet = receiver.get_current_sequence_number()

        full_message = receiver.get_message_by_received_packets()
        print(f"Receiver message: {full_message}")
    else:
        print("Not Sending an Empty String")