import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory


#Başlık ve Açıklamalar
st.set_page_config(page_title="Akıllı Turizm Rehberi", page_icon=":earth_africa:")
st.title("Akıllı Turizm Rehberi")
st.markdown("Türkiye'nin dört bir yanındaki turistik yerler hakkında bilgi almak için sorularınızı sorabilirsiniz.")


#Session State (streamlit de kullanıcı geçmişini tutmak için)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)


#GROQ API KEY'i tanımla
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,  # 0'a yakınsa garanti cevap verir, 1'e yakınsa daha yaratıcı/çeşitli cevap verir, 1'e yaklaştıkça halüsinasyon riski artar
    groq_api_key=st.secrets["GROQ_API_KEY"]
)


#Mesaj kutusu: kullanıcıdan gelen mesaj
user_input = st.chat_input("Bir şehir, mekan, yemek ya da aktivite sorabilirsiniz...")

if user_input:
    #yeni gelen kullanıcı mesajını ilk  olarak memory e ekliyoruz 
    st.session_state.memory.chat_memory.add_user_message(user_input)
    
    #tüm konuşmayı modele verecek şekilde mesajları oluşturalım: sistem mesajı + memory + human message
    messages = [
        SystemMessage(content="Sen bir akıllı turizm rehberisin. Kullanıcıya gezilecek yerler, tatil önerileri, ulaşım bilgileri ve yöresel yemekler gibi konularda yardımcı olmalısın.")
    ] + st.session_state.memory.load_memory_variables({})["history"] + [HumanMessage(content=user_input)]
    
    
    #Modelden yanıt al
    response = llm(messages)
    
    
    #Yanıtı hafızaya kaydet
    st.session_state.memory.chat_memory.add_ai_message(response.content)

#Sohbet geçmişini arayüzde göster
#Tüm mesajları sırasıyla gezip ekrana bastıralım
for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("Kullanıcı"):
            st.markdown(msg.content)
    else:
        with st.chat_message("Akıllı Rehber"):
            st.markdown(msg.content)