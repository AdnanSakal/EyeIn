import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
text = """Assalamualaikum, kemon achen ajke? Boshen. Ki obostha apnar? Waalaikumsalam. Eito, asi motamuti. Raat e ghum bhalo hoyechilo? Sharirik kono problem feel korchen?
Hello, kemon acho? Sharir bhalo tomar? Hmm, eito asi, motamuti.Ami bhalo achi,. Tumi kheyecho Ha baba, ami kheyechi Allah Hafez
Kemon aso? Ami  valo asi. Ki koro. Kisu na.tumi ki koro? Amio kisu kori na.
Kemon aso tumi? Asha kori bhalo aso. Ajke sokale ghum theke uthe mone holo je onekdin dhore ekta boro kotha bola hoy nai. Tumi ki boro busy chhile? Ajke kichu bishes plan ache? Amar mone hocche ekta bhalo cha-khawa ar kichu halka golpo hole khub shanti lagbe. Jodi tumi free thako, tahole boshle ekta bhalo adda hoy. Eto din por abar eirokom ekta shaanto din lagche boro dorkar chhilo
Assalamualaikum, kemon achen ajke? Waalaikumsalam. Ei toh, achi motamuti.shoril Kemon ekhon apnar. Alhamdullilah. Apnar shoril Kemon? Alhamdillilah
Hello Kemon acho? Ami valo achi, tumi Kemon aso? Ami o valo achi. Aajker din ta kemon gelo? bhalo chhilo. Kichu kaj chhilo, kichukhon bondhuder sathe baire gechilam. Baap! Kothay gechila? Amra park e gechilam. Ektu hatahati ar golpo korechilam. Besh moja hoyese! Amar o majhe majhe baire beriye halka hatahathi korte bhalo lage. hmm, prokritir modhye shomoy katate onek bhalo lage. Tumi kothay ghurte pochhondo koro? Ami somudrer dhare jete pochhondo kori. Sekhane shanti onek bhalo lage. Ah, somudro to sotti darun! Ami ekdin somudrer pashe ghurte jabo
kemon aso? Ami valo achi, tumi? Aaj weather to khub bhalo, na? Na beshi gorom, na beshi thanda, ekdum perfect
 kemon achho? Ami valo achi, dhonnobad! Tumi kemon achho? Ami o valo achi. Ki news? Kichu interesting holo?
hmm, actually ami notun ekta book pora shuru korchi. Onek interesting, science fiction genre. Tumi ki korso Ami ekhon nijer vabnay thaki shudhu. Tomar ki oboshta
kemon achho? Kemon poristithi? Ami valo asi, dhonnobad. Tumi Kemon aso? Kibhabe katse din? Ami valo  achi, kintu beshi valo na.
Tumake dekhe khub bhalo laglo.
Assalamualaikum, kemon achen ajke? Waalaikumsalam ami valo asi.kothay theke ashlen.kemon jasse din? Asi motamoti.ki oboshta apnar
"""
load_model = tf.keras.models.load_model("test_model.keras")





tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])
# pad_seq = pad_sequences(input,maxlen = 89,padding = "pre")


def prediction(text):
    output = ""
    for i in range(1):
        tokenize = tokenizer.texts_to_sequences([text])[0]
        pad_token = pad_sequences([tokenize],maxlen=89,padding = "pre")
        pred = np.argmax(load_model.predict(pad_token),axis=-1)
        # pred = tf.random.categorical(model.predict(pad_token)/1,num_samples = 1)[0].numpy()
        for i,l in tokenizer.word_index.items():
            if l == pred:
                text = text+" "+i
                output = text
    return output



    
        
