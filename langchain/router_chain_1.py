from gemini import googleai_client
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains.router import MultiPromptChain
from langchain.chains.llm import LLMChain
from langchain.chains.router.llm_router import (
    LLMRouterChain,
    RouterOutputParser,
)
from langchain.chains.router.multi_prompt_prompt import (
    MULTI_PROMPT_ROUTER_TEMPLATE,
)

llm = googleai_client

quimica_template = ChatPromptTemplate.from_template(
    """Você é um químico experiente, especializado em explicar conceitos de
química de forma clara e objetiva. Seu conhecimento abrange reações químicas,
elementos, compostos e a relação entre estrutura molecular e propriedades dos
materiais. Se não souber a resposta para uma pergunta, você admite isso.

Pergunta: {input}"""
)

geografia_template = ChatPromptTemplate.from_template(
    """Você é um geógrafo com amplo conhecimento sobre processos naturais,
geografia humana, clima, relevo e a interação entre ambiente e sociedade.
Você explica como fatores físicos e humanos moldam o mundo ao nosso redor
de maneira acessível e precisa.

Pergunta: {input}"""
)

biologia_template = ChatPromptTemplate.from_template(
    """Você é um biólogo altamente capacitado, com expertise em seres vivos,
suas estruturas, funções e interações ecológicas. Você é excelente em tornar
conceitos biológicos compreensíveis tanto para iniciantes quanto para
especialistas.

Pergunta: {input}"""
)

prompt_infos = [
    {
        "name": "Química",
        "description": "Ideal para responder pergunta de química",
        "prompt_template": quimica_template,
    },
    {
        "name": "Geografia",
        "description": "Ideal para responder pergunta de geografia",
        "prompt_template": geografia_template,
    },
    {
        "name": "Biologia",
        "description": "Ideal para responder pergunta de biologia",
        "prompt_template": biologia_template,
    },
]

chains_destino = {}
for info in prompt_infos:
    chain = LLMChain(llm=llm, prompt=info["prompt_template"], verbose=True)
    chains_destino[info["name"]] = chain

destinos = [f'{p["name"]}: {p["description"]}' for p in prompt_infos]
destinos_str = "\n".join(destinos)
print(destinos_str)

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinos_str,
)

# print(router_template)

router_template = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

router_chain = LLMRouterChain.from_llm(llm, router_template, verbose=True)

default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=llm, prompt=default_prompt, verbose=True)
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=chains_destino,
    default_chain=default_chain,
    verbose=True,
)

resposta = chain.invoke({"input": "O que é o El Niño?"})
print(resposta)
