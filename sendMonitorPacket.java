public void sendMonitorPacket(Network.Packet packet) {
    try {
        DatagramPacket monitor_packet;

        byte[] type = String.valueOf(packet.getType().getNumber()).getBytes();
        byte[] dataSize = String.valueOf(packet.getSerializedSize()).getBytes();
        byte[] buf = new byte[type.length + 1 + dataSize.length];

        System.arraycopy(type, 0, buf, 0, type.length);
        buf[type.length] = (byte)':';
        System.arraycopy(dataSize, 0, buf, type.length + 1, dataSize.length);

        monitor_packet = new DatagramPacket(buf, buf.length, InetAddress.getByName("localhost"), 8080);
        monitor_socket.send(monitor_packet);
    } catch (Exception e) {
        e.printStackTrace();
    }
}